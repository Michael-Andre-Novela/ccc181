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
    flash(f"You joined the queue. Your ticket number is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((x for x in TICKETS if x["number"] == ticket_id), None)
    if t is None:
        abort(404)

    ahead_count = sum(
        1
        for x in TICKETS
        if x["service_id"] == t["service_id"]
        and x["status"] == "waiting"
        and x["number"] < t["number"]
    )
    service = next((s for s in SERVICES if s["id"] == t["service_id"]), {"name": "General Bag Drop"})
    return render_template("ticket.html", ticket=t, service=service, ahead=ahead_count)


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


if __name__ == "__main__":
    app.run(debug=True)