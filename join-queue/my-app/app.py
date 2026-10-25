"""CCC181 Week 3: NAIA ExpressPass Queue Management System"""

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

SERVICES = [
    {"id": 1, "name": "Virtual Slot Drop-off (Pre-booked)"},
    {"id": 2, "name": "Priority Lane (OFW / Senior / PWD / Infant)"},
    {"id": 3, "name": "Standby / Walk-in Bag Drop"},
]

TICKETS = [
    {
        "number": 1,
        "name": "Ramon Santos",
        "email": "ramon.santos@gmail.com",
        "service_id": 1,
        "flight_number": "5J-501",
        "pnr": "X7K9LP",
        "num_bags": 2,
        "slot_time": "14:15 - 14:30",
        "status": "waiting",
    },
    {
        "number": 2,
        "name": "Maria Clara Reyes",
        "email": "m.reyes@yahoo.com",
        "service_id": 2,
        "flight_number": "PR-1845",
        "pnr": "A2B3C4",
        "num_bags": 1,
        "slot_time": "14:15 - 14:30",
        "status": "waiting",
    },
    {
        "number": 3,
        "name": "Juan Dela Cruz",
        "email": "juan.delacruz@outlook.com",
        "service_id": 3,
        "flight_number": "Z2-763",
        "pnr": "Q9W8E7",
        "num_bags": 3,
        "slot_time": "Walk-in",
        "status": "called",
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    flight_number = form.get("flight_number", "").strip().upper()
    pnr = form.get("pnr", "").strip().upper()
    num_bags = form.get("num_bags", type=int)
    service_id = form.get("service_id", type=int)
    slot_time = form.get("slot_time", "14:15 - 14:30").strip()

    errors = {}
    if not name:
        errors["name"] = "Enter your full name."
    if "@" not in email or "." not in email:
        errors["email"] = "Enter a valid email address."
    if not flight_number:
        errors["flight_number"] = "Enter your flight number (e.g., 5J-501)."
    if not pnr or len(pnr) != 6:
        errors["pnr"] = "Booking reference (PNR) must be exactly 6 characters."
    if not num_bags or num_bags < 1 or num_bags > 5:
        errors["num_bags"] = "Specify between 1 and 5 bags."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service lane."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append(
        {
            "number": number,
            "name": name,
            "email": email,
            "service_id": service_id,
            "flight_number": flight_number,
            "pnr": pnr,
            "num_bags": num_bags,
            "slot_time": slot_time,
            "status": "waiting",
        }
    )
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((x for x in TICKETS if x["number"] == ticket_id), None)
    if t is None:
        abort(404)

    ahead = [
        x for x in TICKETS
        if x["service_id"] == t["service_id"]
        and x["status"] == "waiting"
        and x["number"] < t["number"]
    ]
    service = next((s for s in SERVICES if s["id"] == t["service_id"]), {"name": "General Bag Drop"})
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))


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
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]

    names = {s["id"]: s["name"] for s in SERVICES}

    # ★ Setting-specific feature: Waiting counts per service lane
    counts = {
        s["id"]: sum(1 for t in TICKETS if t["service_id"] == s["id"] and t["status"] == "waiting")
        for s in SERVICES
    }

    first_waiting = next((t for t in queue if t["status"] == "waiting"), None)

    return render_template(
        "staff.html",
        queue=queue,
        services=SERVICES,
        names=names,
        selected=service_id,
        counts=counts,
        first_waiting=first_waiting,
    )


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
    
    # Maintain existing service_id filter if present in query parameters
    service_id = request.args.get("service_id", type=int)
    return redirect(url_for("staff_dashboard", service_id=service_id if service_id else None))


if __name__ == "__main__":
    app.run(debug=True)