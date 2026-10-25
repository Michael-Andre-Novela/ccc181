# Self-Review of Personas and Wireframes

This document contains a self-review of the three main interface screens for **NAIA ExpressPass** (Terminal 3 Bag Drop Queue App), evaluating the wireframes against the design rules established for our personas (**Ramon Santos**, the person waiting, and **Bea Bee**, the ground staff operator).

---

## Screen 1: Join Queue (`/join`)

### Self-Review Questions Assessment
1. **5-second clarity:** Ramon can immediately identify the form fields for Name, Flight #, PNR, Bags, and Preferred Slot.
2. **Status visibility:** N/A for this initial intake screen (status tracking begins after ticket generation).
3. **Real-world terminology:** Uses standard Philippine aviation terms: "Flight Number", "Booking Reference / PNR", "Luggage / Bags", "Priority Lane (OFW / Senior / PWD)", and "Counter".
4. **Primary staff action:** N/A (Passenger-facing screen).
5. **Mobile hierarchy:** Mobile layout displays Step 1 (Dossier), Step 2 (Flight Credentials), and Step 3 (Service Lane Selection) in a single clear vertical column.
6. **Persona design rules check:** Follows Rule 1 (clear flight/slot selection) and Rule 3 (explicit warning on 45-minute cutoff).

### Review
* **Works well:** The multi-step visual grouping (Passenger Dossier, Flight Credentials, Service Lane) and preset slot windows allow Ramon to complete his registration in under 15 seconds even while balancing his luggage trolley with one hand.
* **Problem:** If Ramon mistakenly enters an invalid 5-character PNR code or leaves his flight number empty, submitting without inline feedback forces extra cognitive effort to re-examine the whole form (*Usability Principle: Error Prevention*).
* **Change:** I will keep the current wireframe design layout without modifying the structure. Server-side validation and Jinja alert feedback during implementation (Part 5) will handle invalid PNR formats and missing inputs cleanly without requiring visual wireframe changes.

---

## Screen 2: My Place (`/queue/<id>`)

### Self-Review Questions Assessment
1. **5-second clarity:** The ticket number (`A-014`), status badge (`STATUS: WAITING`), assigned counter (`Assigned to: Counter 4`), and live queue position (`2 passengers ahead`) are immediately recognizable within 2 seconds.
2. **Status visibility:** Prominent badge at the top right of the ticket display clearly indicates state (`WAITING`, `CALLED`, `SERVED`).
3. **Real-world terminology:** Uses exact airport wayfinding terms: "Counter 4", "Departure Hall Level 3", "Pillar 7", "Flight 5J-501", and "Boarding Gate".
4. **Primary staff action:** N/A (Passenger-facing status screen).
5. **Mobile hierarchy:** Ticket number, assigned counter, and live position count ("2 passengers ahead") are positioned above the fold.
6. **Persona design rules check:** Follows Ramon's Rule 1 (giant ticket number and counter location) and Rule 2 (live updating status).

### Review
* **Works well:** Placing the giant ticket number (`A-014`), assigned counter location (`Counter 4 - Opposite Pillar 7`), and live position count right at the top ensures Ramon can check his exact turn at a glance while walking through a noisy, congested terminal.
* **Problem:** Ramon might worry whether his ticket status is actively updating or frozen due to weak airport Wi-Fi (*Usability Principle: Visibility of System Status*).
* **Change:** I will keep the wireframe layout exactly as drawn. The auto-refreshing JavaScript polling mechanism built in Part 8 (`/queue/<id>/status.json`) will continuously update the page and provide real-time status feedback without altering the visual structure.

---

## Screen 3: Staff Dashboard (`/staff`)

### Self-Review Questions Assessment
1. **5-second clarity:** Bea Bee can instantly view the active queue count (`4 pax`), currently served ticket (`A-012`), and upcoming passengers in order.
2. **Status visibility:** Every row and card clearly displays a status tag (`WAITING`, `CALLED`, `SERVED`, `NO-SHOW`).
3. **Real-world terminology:** Matches ground ops vocabulary: "Desk 4B", "Inducting Bags", "Pax", "PNR", "Scale Weigh-In", and "Belt 4".
4. **Primary staff action:** The primary button **"CALL NEXT PASSENGER"** is styled as the largest, most prominent action button on both mobile and desktop viewports.
5. **Mobile hierarchy:** Mobile view stacks each passenger entry into a distinct card with large touch targets for `CALL`, `SERVE`, and `NO-SHOW`.
6. **Persona design rules check:** Follows Bea Bee's Rule 1 (one-click action buttons) and Rule 2 (prominent Flight #, PNR, and bag counts per entry).

### Review
* **Works well:** The dedicated high-contrast **"CALL NEXT PASSENGER"** button and inline action buttons (`CALL`, `SERVE`, `NO-SHOW`) for each passenger allow Bea Bee to advance the queue with a single click without taking her eyes off the physical baggage belt.
* **Problem:** During peak flight rushes with multiple overlapping departures, Bea Bee could accidentally click "Serve" on the wrong passenger row (*Usability Principle: Error Prevention*).
* **Change:** I will keep the wireframe structure exactly as designed. The card layout on mobile and the structured table row layout on desktop provide ample spacing between buttons, preventing accidental misclicks while preserving fast 1-click execution.

---

### Checkpoint 3 Summary
- [x] All three screens evaluated in the required *Works well / Problem / Change* format.
- [x] Identified usability principles for each screen (Error Prevention, Visibility of System Status).
- [x] Documented clear rationale for keeping the wireframe layouts intact.