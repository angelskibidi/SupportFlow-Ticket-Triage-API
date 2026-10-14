# IBM Job Fair Preparation

## Resume project entry

**SupportFlow Ticket Triage API** — Python, Flask, SQLite, pytest, Docker, REST APIs, Git

- Built a Flask REST API for creating, updating, filtering, and deleting software-support tickets with SQLite persistence and input validation.
- Wrote 7 pytest tests covering health checks, CRUD behavior, filtering, invalid input, and 404 errors; debugged the test setup until all tests passed.
- Added a lightweight browser dashboard and Docker configuration to make the service repeatable to run locally.

Use these bullets only after you understand and can demonstrate the project. The resume guide recommends showing how and why you used the keywords, keeping project bullets focused, and limiting the project to three bullets.

## IBM keyword match

| IBM qualification | Evidence in this project |
|---|---|
| Software development | Flask routes, validation, database layer, and dashboard |
| REST APIs | GET, POST, PATCH, and DELETE endpoints |
| Databases | SQLite table, constraints, queries, and filters |
| Git/version control | Put the project in a Git repository and make small commits as you improve it |
| Testing/debugging | 7 pytest tests, including invalid input and missing-ticket cases |
| Cloud/container interest | Dockerfile and repeatable container command |
| Analytical problem-solving | Ticket status/priority model and validation rules |
| Agile/collaboration | Explain the project as small iterations: API, validation, tests, UI, packaging |

## Thirty-second introduction

“Hi, I’m Angel Sanchez, a computer science student interested in the Software Developer co-op. I’ve been building my fundamentals in C++ through data structures, algorithms, and ADTs, and I recently built a small Python/Flask ticket-triage service. It uses REST endpoints, SQLite, pytest, and Docker. I’m especially interested in IBM because the co-op emphasizes learning modern development practices and contributing to real software projects. What kinds of software projects do co-op students typically join on your team?”

## If they ask about the project

“I chose a ticket-triage system because it gave me a realistic CRUD problem. I separated route handling, validation, persistence, and testing. The API supports filtering by status and priority, and I tested both successful requests and failures such as invalid priority values and missing ticket IDs. The next feature I would add is authentication and a production database such as PostgreSQL.”

## Good questions to ask IBM

- “What does a successful first month look like for a Software Developer co-op on your team?”
- “How are co-op students paired with mentors and included in code reviews?”
- “Which technologies or development practices would you recommend I learn before the co-op begins?”
- “Does the team work more on backend services, user interfaces, or full-stack features?”

## Closing line

“Thank you for explaining that. I’m very interested in the co-op, and I’d appreciate your advice on which part of my background would be most useful for this role. May I connect with you on LinkedIn and apply using the IBM requisition?”

## What to avoid saying

- Do not call the project “production-ready.”
- Do not claim cloud deployment, Kubernetes, CI/CD, or team collaboration unless you actually add and use them.
- Do not list a technology just because it appears in the IBM posting; be ready to explain how you used every tool on your resume.
