"""CCC181 Week 4: NAIA ExpressPass Queue Management System"""

import os

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)



@app.route("/")
def index():
    return render_template("index.html")


def all_services():
    return db.session.scalars(
        db.select(Service).order_by(Service.name)
    ).all()
    
PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)

@app.get("/join")
def join_form():
    return render_template(
        "join.html",
        services=all_services(),
        form={},
        errors={}
    )


@app.post("/join")
def join():
    form = request.form

    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    flight_number = form.get("flight_number", "").strip().upper()
    pnr = form.get("pnr", "").strip().upper()
    num_bags = form.get("num_bags", type=int)
    service_id = form.get("service_id", type=int)
    slot_time = form.get("slot_time", "").strip()

    service = db.session.get(Service, service_id) if service_id else None

    errors = {}

    if not name or len(name) > 120:
        errors["name"] = "Enter your full name."

    if "@" not in email or "." not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address."

    if not flight_number or len(flight_number) > 12:
        errors["flight_number"] = "Enter your flight number (e.g., 5J-501)."

    if not pnr or len(pnr) != 6:
        errors["pnr"] = "Booking reference (PNR) must be exactly 6 characters."

    if not num_bags or num_bags < 1 or num_bags > 5:
        errors["num_bags"] = "Specify between 1 and 5 bags."

    if service is None:
        errors["service_id"] = "Choose a service lane."

    slot_starts = {
        "14:15 - 14:30": "14:15",
        "14:30 - 14:45": "14:30",
        "14:45 - 15:00": "14:45",
    }

    if slot_time not in slot_starts:
        errors["slot_time"] = "Choose a valid preferred slot."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors=errors
        ), 400

    preferred_slot_at = datetime.strptime(
    f"{datetime.now(PH_TIME).date()} {slot_starts[slot_time]}",
    "%Y-%m-%d %H:%M").replace(tzinfo=PH_TIME)

    user = db.session.scalar(
        db.select(User).filter_by(email=email)
    )

    if user is None:
        user = User(
            name=name,
            email=email
        )

    ticket = Ticket(
        user=user,
        service=service,
        flight_number=flight_number,
        pnr=pnr,
        bag_count=num_bags,
        preferred_slot_at=preferred_slot_at,
    )

    db.session.add(ticket)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(
            "Something went wrong saving your ticket. Please try again.",
            "danger"
        )
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors={}
        ), 409

    flash(
        f"You joined the queue. Your ticket is #{ticket.id}.",
        "success"
    )

    return redirect(
        url_for("ticket", ticket_id=ticket.id)
    )


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=t, service=t.service,
                           ahead=people_ahead(t))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t)}


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = next((x for x in TICKETS if x["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash("You have left the queue.", "info")
    return redirect(url_for("index"))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    return render_template("staff.html", queue=queue, services=all_services(),
                           selected=service_id)


@app.post("/staff/call-next")
def call_next():
    service_id = request.args.get("service_id", type=int)
    waiting = [t for t in TICKETS if t["status"] == "waiting"]
    if service_id:
        waiting = [t for t in waiting if t["service_id"] == service_id]

    if waiting:
        first = waiting[0]
        first["status"] = "called"
        flash(f"Ticket #{first['number']} marked called.", "info")
    else:
        flash("No passengers currently waiting in queue.", "warning")

    return redirect(url_for("staff_dashboard", service_id=service_id if service_id else None))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)

    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")

    service_id = request.args.get("service_id", type=int)
    return redirect(url_for("staff_dashboard", service_id=service_id if service_id else None))

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("Virtual Slot Drop-off (Pre-booked)", 10),
        ("Priority Lane (OFW / Senior / PWD / Infant)", 10),
        ("Standby / Walk-in Bag Drop", 10),
    ]

    for name, minutes in starting:
        exists = db.session.scalar(
            db.select(Service).filter_by(name=name)
        )
        if exists is None:
            db.session.add(
                Service(name=name, avg_minutes=minutes)
            )

    db.session.commit()
    print("Services are ready.")
    
if __name__ == "__main__":
    app.run(debug=True)