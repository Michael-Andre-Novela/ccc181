# Usability Test Report — NAIA ExpressPass

**Tester Profile:** Raven Joy Avenido (3rd-year IT Student) — representing the passenger persona (*Ramon Santos*).  
**Test Setup:** In-person user observation on a mobile viewport (375 px width) connected via local Wi-Fi (`flask --app app run --debug --host 0.0.0.0`).  
**Consent:** Explicit permission granted for screen observation and feedback recording.

---

## 10a. Task Execution & Observations

### Task 1: "You just arrived. Get in line for Virtual Slot Drop-off."
* **Did they finish it?** Yes (Unassisted)
* **Time Taken:** ~18 seconds
* **Hesitations & Verbal Feedback:** 
  - Raven tapped **Join Bag Drop Queue** immediately from the landing hero section.
  - On `/join`, she paused briefly when selecting between the service lane option cards before picking *Virtual Slot Drop-off*.
  - *Quote:* *"Nakalagay pala na 6 characters yung PNR reference! At least alam ko agad kung anong code kukunin sa flight email ko, diba?"*
* **Persona Rule Evaluation:** 
  - **Rule Held Up:** *"Because passengers are in a hurry at the airport, input fields must be clear with immediate validation."* Explicit input format hints and pre-filled bag counts prevented validation errors.

---

### Task 2: "How many people are ahead of you? What is your number?"
* **Did they finish it?** Yes (Unassisted)
* **Time Taken:** ~4 seconds
* **Hesitations & Verbal Feedback:**
  - Located ticket number `#4` instantly due to the large display heading (`display-1 fw-bold`).
  - Read position immediately from the blue callout banner (*"0 people ahead of you / You're next!"*).
  - *Quote:* *"laki ng ticket number! Hindi mamiss kahit nagmamadali kang maglakad sa terminal."*
* **Persona Rule Evaluation:**
  - **Rule Held Up:** *"Because passengers check their status while walking through crowded terminals, status and position text must be high-contrast and prominent."*

---

### Task 3: "Pretend you are the staff member. Call the next person and mark them as served."
* **Did they finish it?** Yes (With minor navigation hesitation)
* **Time Taken:** ~22 seconds
* **Hesitations & Verbal Feedback:**
  - On the passenger ticket page, Raven looked for a direct link to the staff portal. She clicked the navbar brand logo to return to the home page, then selected **Staff Dashboard**.
  - On `/staff`, she immediately tapped the prominent gold **Call next** button.
  - She then clicked the green **Serve** button on the active passenger row in the intake manifest.
  - *Quote:* *"clear ng 'Call Next' button sa taas! Pero try mo din maglagay ng direct staff link sa footer or navbar para hindi na kailangan bumalik sa home page to test."*
* **Persona Rule Evaluation:**
  - **Rule Held Up:** *"Because ground staff process dozens of bags per hour, primary counter actions must take no more than 1 click."*
  - **Rule Needed Adjustment:** *"Because users navigate between roles during testing, system views should provide intuitive context routing."*

---

## 10b. One Key Improvement

### Problem Identified
During Task 3, Raven experienced navigation friction when trying to switch from the passenger ticket view (`/queue/<id>`) to the staff dashboard (`/staff`). The interface lacked a direct link to the staff portal on inner pages, forcing users to navigate back to the homepage first before accessing counter operations.

### Applied Fix
Added a persistent **Staff Portal Quick Link** in the global site footer (`templates/base.html`), enabling ground staff and testers to navigate directly to `/staff` from any screen in 1 click.

### Before & After Comparison
* **Before (`screenshots/usability-before.png`):** The global footer on inner screens (such as `/queue/<id>`) contained only static copyright text, requiring users to navigate back to the homepage (`/`) to find the Staff Dashboard link.
* **After (`screenshots/usability-after.png`):** The updated footer features a persistent **Staff Portal Quick Link** with an explicit icon (`bi-person-badge`) and bold focus outline, allowing seamless 1-click routing to counter operations from any page.