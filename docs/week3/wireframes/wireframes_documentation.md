# NAIA ExpressPass: Wireframe Frames & User Flows

This document details the six wireframe frames designed for **NAIA ExpressPass** across mobile and desktop viewports, mapped to their respective user personas, requirement IDs, and annotated user flows.

## 1. Join Queue Screen (`FR-01`)

### Frame 1: Join Queue — Mobile View

* **Filename:** `docs/week3/wireframes/join_queue_naia_expresspass_wireframe.png`
* **Persona:** Ramon Santos
* **Device:** Smartphone (375 px)
* **Requirement ID:** `FR-01`
* **User Flow:**
  `1. Open /join` → `2. Enter flight details & PNR` → `3. Select 14:15-14:30 slot` → `4. Tap "Get a Ticket"` → `5. Redirect to My Place`

#### Labeled Elements:

* **Header:** NAIA ExpressPass brand logo & collapsible hamburger menu button (`[ ☰ ]`)
* **Page Title:** "Join Bag Drop Queue — NAIA Terminal 3"
* **Form Inputs:**
  * Name (`type="text"`)
  * Email (`type="email"`)
  * Flight Number (`type="text"`, e.g., `5J-501`)
  * Booking Reference / PNR (`type="text"`, 6-character code)
  * Number of Bags (`type="number"`, 1–5)
  * Bag Drop Service Lane (Radio buttons: *Virtual Slot*, *Priority*, *Walk-in*)
  * Preferred Slot Window (Dropdown select, e.g., `14:15 - 14:30`)
* **Action Button:** Full-width primary button "Get a Ticket"

---

### Frame 2: Join Queue — Desktop View

* **Filename:** `docs/week3/wireframes/join_queue_desktop_portal_wireframe.png`
* **Persona:** Ramon Santos
* **Device:** Laptop / Desktop (1440 px)
* **Requirement ID:** `FR-01`
* **User Flow:**
  `1. Open /join` → `2. Complete 2-column form card` → `3. Click "Get a Ticket"` → `4. Redirect to My Place`

#### Labeled Elements:

* **Top Navigation Bar:** Brand header with navigation links (*Join Queue*, *Staff*)
* **Form Container:** Centered Bootstrap card container
* **Two-Column Input Grid:**
  * Left Column: Full Name, Email Address, Service Lane Dropdown
  * Right Column: Flight Number, PNR Code, Number of Bags, Preferred Slot Time
* **Action Button:** Centered primary button "Get a Ticket"

---

## 2. My Place Screen (`FR-02`)

### Frame 3: My Place — Mobile View

* **Filename:** `docs/week3/wireframes/my_ticket_queue_status_wireframe.png`
* **Persona:** Ramon Santos
* **Device:** Smartphone (375 px)
* **Requirement ID:** `FR-02`
* **User Flow:**
  `1. Arrive from join redirect` → `2. View large Ticket # A-014 & Counter 4` → `3. Read "2 passengers ahead"` → `4. Auto-update to "Called"`

#### Labeled Elements:

* **Flashed Alert Banner:** Green success alert ("You joined the queue. Your ticket is #1.")
* **Main Ticket Card:**
  * Ticket Number Header (`display-1 fw-bold` text: **A-014**)
  * Status Badge (`Waiting` - Warning yellow badge)
  * Assigned Counter (`Counter 4`)
  * Flight Metadata Summary (Flight: `5J-501` | PNR: `X7K9LP` | Bags: `2`)
  * Reserved Slot Window (`14:15 - 14:30`)
* **Live Position Indicator Box:** High-contrast box stating *"2 passengers ahead of you in line."*
* **Action Button:** Red outline button "Leave Queue / Cancel Ticket"

---

### Frame 4: My Place — Desktop View

* **Filename:** `docs/week3/wireframes/my_ticket_desktop_status_wireframe.png`
* **Persona:** Ramon Santos
* **Device:** Laptop / Desktop (1440 px)
* **Requirement ID:** `FR-02`
* **User Flow:**
  `1. View active ticket card` → `2. Verify flight & slot window` → `3. Track live queue position`

#### Labeled Elements:

* **Top Navigation Bar:** Active page context highlight on "Join Queue"
* **Centered Ticket Display:**
  * Ticket Number (**A-014**) aligned with right-hand Status Badge (`Waiting`)
  * Full details list: Counter assignment, Service Lane, Flight Number, PNR Code, Checked Bags, and Reserved Time Window
* **Live Position Banner:** Wide alert box displaying real-time count of waiting passengers ahead
* **Action Button:** Cancel / Leave queue button

---

## 3. Staff Dashboard Screen (`FR-03`)

### Frame 5: Staff Dashboard — Mobile View

* **Filename:** `docs/week3/wireframes/staff_counter_4_dashboard_wireframe.png`
* **Persona:** Bea Bee
* **Device:** Phone / Tablet (375 px)
* **Requirement ID:** `FR-03`
* **User Flow:**
  `1. Open /staff` → `2. Filter by Virtual Slot lane` → `3. Tap "Call Next"` → `4. Scroll table right & tap "Serve"`

#### Labeled Elements:

* **Header:** NAIA ExpressPass Counter 4 Staff View
* **Summary Bar:** Total Active Waiting Passengers count
* **Primary Counter Action:** Prominent full-width button "Call Next Ticket"
* **Service Filter Pills:** Horizontal filter buttons (*All*, *Virtual Slot*, *Priority*, *Walk-in*)
* **Responsive Table Container (`.table-responsive`):** Horizontal scrollable table showing Ticket #, Flight #, Status, and Action buttons (*Call*, *Serve*)

---

### Frame 6: Staff Dashboard — Desktop View

* **Filename:** `docs/week3/wireframes/staff_counter_portal_desktop_dashboard_wireframe.png`
* **Persona:** Bea Bee
* **Device:** Laptop / Desktop (1440 px)
* **Requirement ID:** `FR-03`
* **User Flow:**
  `1. Open /staff dashboard` → `2. Filter by service lane` → `3. Click "Call Next"` → `4. Verify PNR & click "Serve"`

#### Labeled Elements:

* **Counter Header:** Ground Operations Counter Dashboard — NAIA Terminal 3 (Counter 4)
* **Top Control Bar:** Service lane filter dropdown menu paired with the "Call Next Passenger" primary button
* **Operations Table:**
  * Table Headers (`th scope="col"`): `Ticket #`, `Passenger Name`, `Flight #`, `PNR`, `Bags`, `Slot Window`, `Status`, `Actions`
  * Table Rows: Color-coded status badges (`Waiting`, `Called`, `Served`)
  * Inline Action Form Buttons: Small "Call", "Serve", and "No-Show" action triggers per ticket row