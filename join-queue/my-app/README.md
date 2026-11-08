# NAIA ExpressPass: Terminal 3 Queue App

Queue management app for **CCC181**.  
It handles passenger bag-drop reservations and staff queue operations at NAIA Terminal 3.

## Project structure

```text
ccc181/
├── .env                  # local database credentials (not committed)
├── .env.example          # example environment variables
├── .gitignore            # keeps secrets and local files out of Git
├── compose.yaml          # PostgreSQL Docker configuration
├── docs/
│   ├── requirements.md
│   ├── week3/
│   └── week4/
│       ├── erd.png
│       ├── schema.md
│       └── schema-review.md
└── join-queue/
    ├── DEMO.md
    └── my-app/
        ├── app.py              # creates the app and defines routes
        ├── models.py           # SQLAlchemy database models
        ├── requirements.txt    # packages to rebuild the environment
        ├── migrations/         # Alembic database migrations
        ├── .venv/              # virtual environment (not committed)
        ├── templates/          # Jinja2 HTML files
        │   ├── base.html
        │   ├── index.html
        │   ├── join.html
        │   ├── ticket.html
        │   ├── staff.html
        │   └── services.html
        └── static/
            ├── css/style.css
            └── js/main.js
```

## Routes

| URL | Method | View function | What you see |
|---|---|---|---|
| `/` | GET | `index()` | Welcome page with system overview and "Join the queue" button |
| `/join` | GET | `join_form()` | Form to join the queue |
| `/join` | POST | `join()` | Validates the form and saves a ticket to PostgreSQL |
| `/queue/<int:ticket_id>` | GET | `ticket()` | Ticket status and number of passengers ahead |
| `/queue/<int:ticket_id>/status.json` | GET | `ticket_status()` | JSON endpoint returning current status and number ahead |
| `/queue/<int:ticket_id>/leave` | POST | `leave()` | Leaves the queue while keeping the ticket record |
| `/staff` | GET | `staff_dashboard()` | Staff dashboard with service filtering |
| `/staff/call-next` | POST | `call_next()` | Calls the next waiting passenger |
| `/staff/tickets/<int:ticket_id>/<action>` | POST | `staff_action()` | Calls, serves, or marks a ticket as no-show |
| `/staff/tickets/<int:ticket_id>/delete` | POST | `delete_ticket()` | Permanently deletes a ticket |
| `/staff/services` | GET | `services_list()` | Displays the Manage Services page |
| `/staff/services` | POST | `service_create()` | Creates a new service |
| `/staff/services/<int:service_id>/edit` | POST | `service_edit()` | Updates a service |
| `/staff/services/<int:service_id>/delete` | POST | `service_delete()` | Deletes a service with no existing tickets |

## 1. Set up the Python environment

```bash
cd join-queue/my-app

# create (once per project)
python -m venv .venv

# activate (every new terminal)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# install the packages
pip install -r requirements.txt
```

Your prompt shows `(.venv)` when the environment is active. Some systems use `python3` or `py` instead of `python`.

If PowerShell blocks the activate script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If you add more packages later, record them with:

```bash
pip freeze > requirements.txt
```

## 2. Set up PostgreSQL

NAIA ExpressPass uses PostgreSQL 17 through Docker Compose.

Copy `.env.example` to `.env` and provide your local PostgreSQL password.

Example:

```env
POSTGRES_PASSWORD=your-postgres-password
DATABASE_URL=postgresql+psycopg://naiaexpresspass:your-postgres-password@localhost:5432/naiaexpresspass
```

The real `.env` file is ignored by Git and should never be committed.

From the repository root, start PostgreSQL:

```bash
docker compose up -d
```

Check that it is running:

```bash
docker compose ps
```

## 3. Prepare the database

With the virtual environment active inside `join-queue/my-app`, apply the database migrations:

```bash
flask --app app db upgrade
```

Add the starting services:

```bash
flask --app app seed
```

The seed command can be run more than once without adding duplicate starting services.

The application uses three main database tables:

- `users` — passenger and staff information
- `services` — available baggage-drop services
- `tickets` — passenger queue entries

Database changes are managed using Flask-Migrate and Alembic.

## 4. Run the app

```bash
flask --app app run --debug
```

Open `http://127.0.0.1:5000`.

With `--debug`, the server reloads every time you save a file. Never use debug mode in production.

Passenger tickets, services, and queue status are stored in PostgreSQL and remain available after Flask restarts.

## 5. Database commands

Open PostgreSQL from the repository root:

```bash
docker compose exec db psql -U naiaexpresspass
```

List the tables:

```sql
\dt
```

Inspect the tickets table:

```sql
\d tickets
```

View the services:

```sql
SELECT * FROM services ORDER BY id;
```

View the tickets:

```sql
SELECT id, user_id, service_id, status, created_at, called_at
FROM tickets
ORDER BY id;
```

Exit PostgreSQL:

```sql
\q
```

## 6. Database migrations

When the database models intentionally change, create a migration:

```bash
flask --app app db migrate -m "describe the change"
```

Review the generated migration before applying it.

Apply it with:

```bash
flask --app app db upgrade
```

Undo the latest migration with:

```bash
flask --app app db downgrade
```

The project currently includes the initial database migration and a second migration for the service `active` field.

## 7. Put it on GitHub

### Once per computer

```bash
git config --global user.name "Your Name"
git config --global user.email you@g.msuiit.edu.ph
git config --list
```

### Clone the repository

```bash
git clone https://github.com/Michael-Andre-Novela/ccc181.git
cd ccc181
```

Repository:

https://github.com/Michael-Andre-Novela/ccc181

### Everyday loop

```bash
git pull
git status
git add <file>
git commit -m "Describe your change"
git push
```

## 8. Week 4 database branch

The Week 4 database work is developed on:

```text
feature/week4-database
```

To switch to the branch:

```bash
git switch feature/week4-database
```

The database implementation replaces the temporary Python `SERVICES` and `TICKETS` lists used in the earlier version of the application.

Passenger queue submissions are now saved to PostgreSQL. Existing users are reused based on their email address, while each queue submission creates a ticket connected to a user and service.

The staff dashboard reads queue data from PostgreSQL. Staff can call passengers, serve tickets, mark no-shows, delete mistaken tickets, and manage available services.

Leaving the queue changes the ticket status to `left` instead of deleting the record.

Inactive services remain stored in the database but are not displayed on the passenger join form.

## 9. Staff service management

Staff can open:

```text
/staff/services
```

From this page, staff can:

- add a service
- edit a service name
- change its average processing time
- activate or deactivate it
- view its ticket count
- delete a service with no tickets

A service with existing tickets cannot be deleted. It should be deactivated instead so existing ticket history remains valid.

## Staff route security

Staff routes are currently unprotected for the database implementation.

Staff login and route protection will be added in Week 11.

GitHub issue:

```text
Protect staff routes (Week 11)
```

## Commit message tips

- Short summary in the imperative: "Add...", "Fix..."
- One logical change per commit
- Commit early and often
- Good: "Add database-backed staff actions"
- Unhelpful: "update", "asdf", "final na talaga"