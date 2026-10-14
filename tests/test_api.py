import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture()
def client(tmp_path, monkeypatch):
    database = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(database))

    import app as ticket_app

    ticket_app.DATABASE = database
    ticket_app.initialize_database()
    ticket_app.app.config.update(TESTING=True)
    with ticket_app.app.test_client() as test_client:
        yield test_client


def create_sample(client):
    return client.post(
        "/api/tickets",
        json={
            "title": "Login button fails",
            "description": "The login button returns an error on mobile.",
            "priority": "high",
        },
    )


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_create_and_get_ticket(client):
    created = create_sample(client)
    assert created.status_code == 201
    ticket_id = created.json["id"]

    response = client.get(f"/api/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json["priority"] == "high"
    assert response.json["status"] == "open"


def test_rejects_invalid_priority(client):
    response = client.post(
        "/api/tickets",
        json={"title": "Bug", "description": "Details", "priority": "urgent"},
    )
    assert response.status_code == 400
    assert "priority" in response.json["error"]


def test_filters_tickets_by_status(client):
    create_sample(client)
    second = create_sample(client)
    client.patch(f"/api/tickets/{second.json['id']}", json={"status": "closed"})

    response = client.get("/api/tickets?status=closed")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["status"] == "closed"


def test_updates_ticket(client):
    created = create_sample(client)
    response = client.patch(f"/api/tickets/{created.json['id']}", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json["status"] == "in_progress"


def test_missing_ticket_returns_404(client):
    response = client.get("/api/tickets/999")
    assert response.status_code == 404


def test_deletes_ticket(client):
    created = create_sample(client)
    ticket_id = created.json["id"]
    response = client.delete(f"/api/tickets/{ticket_id}")
    assert response.status_code == 200
    assert client.get(f"/api/tickets/{ticket_id}").status_code == 404
