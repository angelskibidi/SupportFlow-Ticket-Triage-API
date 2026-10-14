from pathlib import Path
import os
import sqlite3

from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).parent
DATABASE = Path(os.getenv("DATABASE_PATH", BASE_DIR / "tickets.db"))

app = Flask(__name__, static_folder="static")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high')),
                status TEXT NOT NULL CHECK(status IN ('open', 'in_progress', 'closed')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def ticket_to_dict(ticket):
    return dict(ticket)


def validate_ticket(data, partial=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    required = ["title", "description", "priority"]
    if not partial:
        missing = [field for field in required if field not in data]
        if missing:
            return f"Missing required field(s): {', '.join(missing)}."

    if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
        return "title must be a non-empty string."
    if "description" in data and (not isinstance(data["description"], str) or not data["description"].strip()):
        return "description must be a non-empty string."
    if "priority" in data and data["priority"] not in {"low", "medium", "high"}:
        return "priority must be low, medium, or high."
    if "status" in data and data["status"] not in {"open", "in_progress", "closed"}:
        return "status must be open, in_progress, or closed."
    return None


@app.get("/")
def dashboard():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/health")
def health_check():
    return jsonify({"status": "ok"})


@app.get("/api/tickets")
def list_tickets():
    status = request.args.get("status")
    priority = request.args.get("priority")
    query = "SELECT * FROM tickets WHERE 1=1"
    parameters = []

    if status:
        query += " AND status = ?"
        parameters.append(status)
    if priority:
        query += " AND priority = ?"
        parameters.append(priority)
    query += " ORDER BY id DESC"

    with get_connection() as connection:
        tickets = connection.execute(query, parameters).fetchall()
    return jsonify([ticket_to_dict(ticket) for ticket in tickets])


@app.post("/api/tickets")
def create_ticket():
    data = request.get_json(silent=True)
    error = validate_ticket(data)
    if error:
        return jsonify({"error": error}), 400

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tickets (title, description, priority, status) VALUES (?, ?, ?, ?)",
            (data["title"].strip(), data["description"].strip(), data["priority"], data.get("status", "open")),
        )
        ticket = connection.execute("SELECT * FROM tickets WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(ticket_to_dict(ticket)), 201


@app.get("/api/tickets/<int:ticket_id>")
def get_ticket(ticket_id):
    with get_connection() as connection:
        ticket = connection.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if ticket is None:
        return jsonify({"error": "Ticket not found."}), 404
    return jsonify(ticket_to_dict(ticket))


@app.patch("/api/tickets/<int:ticket_id>")
def update_ticket(ticket_id):
    data = request.get_json(silent=True)
    error = validate_ticket(data, partial=True)
    if error:
        return jsonify({"error": error}), 400
    if not data:
        return jsonify({"error": "At least one field is required."}), 400

    allowed = {"title", "description", "priority", "status"}
    updates = [(field, data[field].strip() if isinstance(data[field], str) else data[field]) for field in data if field in allowed]
    if not updates:
        return jsonify({"error": "No editable fields were provided."}), 400

    set_clause = ", ".join(f"{field} = ?" for field, _ in updates)
    values = [value for _, value in updates] + [ticket_id]
    with get_connection() as connection:
        cursor = connection.execute(f"UPDATE tickets SET {set_clause} WHERE id = ?", values)
        ticket = connection.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if cursor.rowcount == 0:
        return jsonify({"error": "Ticket not found."}), 404
    return jsonify(ticket_to_dict(ticket))


@app.delete("/api/tickets/<int:ticket_id>")
def delete_ticket(ticket_id):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    if cursor.rowcount == 0:
        return jsonify({"error": "Ticket not found."}), 404
    return jsonify({"message": "Ticket deleted."})


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
