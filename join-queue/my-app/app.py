"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# Sample data for the demo. It lives in memory, so it resets every time the
# server restarts. A real app would save tickets in a database later.
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
    {
        "number": 4,
        "name": "Elena Torres",
        "email": "elena.t@gmail.com",
        "service_id": 1,
        "flight_number": "5J-501",
        "pnr": "M4N5O6",
        "num_bags": 2,
        "slot_time": "14:30 - 14:45",
        "status": "served",
    },
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number


@app.route("/join", methods=["GET", "POST"])
def join():
    # GET: show the empty form. POST: the form was submitted.
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("join.html", error="Please enter your name.")

        number = TICKETS[-1]["number"] + 1 if TICKETS else 1
        TICKETS.append({"number": number, "name": name})
        # Redirect after POST so refreshing the page doesn't join twice.
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
