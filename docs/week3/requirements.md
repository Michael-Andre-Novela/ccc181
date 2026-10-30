
# NAIA ExpressPass requirements

## 1a. Describe your setting and the problem

**Setting:** NAIA Terminal 3 Departures Hall, baggage drop-off counters.

**People who wait:** Departing passengers, including Overseas Filipino Workers (OFWs), senior citizens, persons with disabilities (PWDs), passengers with infants, and walk-in travelers. See the [Ramon Santos passenger persona](week3/personas.md).

**People who serve:** Ground operations staff managing baggage drop-off counters and passenger queues. See the [Bea Bee staff persona](week3/personas.md).

**Problem statement:** Passengers at NAIA Terminal 3 face unpredictable baggage drop-off queues, crowded waiting areas, and the risk of losing valuable time before their flights. They need a simple way to join a queue, view their position, and monitor their status without standing continuously in line. Ground staff need an efficient way to view passenger information, organize queues by service lane, call passengers, and record completed or missed baggage drop-offs.

The Week 3 [usability test](week3/usability-test.md) showed that the basic passenger tasks were understandable, while also identifying navigation friction when switching to the staff dashboard.

## 1b. Functional requirements

★ indicates a requirement specific to the NAIA baggage drop-off setting.

**Priority:** Must, Should, Could, or Won't (this semester).

**Stores data?** indicates whether information must remain available after restarting the application.

**Status:** Built (Week 3), This week, Later, or Dropped. Features marked Built (Week 3) currently use in-memory lists rather than PostgreSQL.

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A passenger can join the baggage drop-off queue by entering a name and email address. | Must | Yes | Built (Week 3) |
| FR-02 ★ | A passenger can provide a flight number, a six-character booking reference (PNR), and a checked-bag count from 1 to 5. | Must | Yes | Built (Week 3) |
| FR-03 ★ | A passenger can select a baggage drop-off lane: Virtual Slot Drop-off, Priority Lane, or Standby / Walk-in Bag Drop. | Must | Yes | Built (Week 3) |
| FR-04 ★ | A passenger can enter a preferred baggage drop-off time window and view it on their ticket. | Must | Yes | Built (Week 3) |
| FR-05 | A passenger can view their ticket number, queue status, selected lane, and number of waiting passengers ahead. | Must | Yes | Built (Week 3) |
| FR-06 | A passenger can receive updated queue status and position information without manually reloading the ticket page. | Must | Yes | Built (Week 3) |
| FR-07 | A passenger can leave the queue while retaining the ticket record with a distinct `left` status. | Must | Yes | This week |
| FR-08 | A ground staff member can view active queue tickets and filter them by service lane. | Must | Yes | Built (Week 3) |
| FR-09 | A ground staff member can call the next waiting passenger in a selected lane and change the ticket status to `called`. | Must | Yes | Built (Week 3) |
| FR-10 | A ground staff member can mark a passenger ticket as `served` or `no-show`. | Must | Yes | Built (Week 3) |
| FR-11 ★ | A ground staff member can view a queued passenger's flight number, PNR, number of bags, and preferred slot window. | Must | Yes | Built (Week 3) |
| FR-12 | A ground staff member can create a service lane, update its name and average service time, and deactivate it for new queue entries. | Must | Yes | This week |
| FR-13 | A ground staff member can permanently delete an incorrectly created ticket after confirming the action. | Must | Yes | This week |
| FR-14 | A ground staff member can delete a service lane only when no tickets reference that lane. | Must | Yes | This week |
| FR-15 | A ground staff member can view daily counts of passengers who left the queue before being served, grouped by lane. | Should | Yes | Later |
| FR-16 ★ | A passenger can reserve a confirmed baggage drop-off slot only when the selected time window has available capacity. | Could | Yes | Later |
| FR-17 ★ | A ground staff member can verify a passenger's eligibility for priority-lane service. | Could | Yes | Later |

### Existing implementation limitations

The Week 3 version of NAIA ExpressPass uses Python lists to store services and tickets. This means queue data does not reliably survive application restarts.

Although passengers can enter a preferred slot window, the application does not currently check slot capacity or guarantee a reservation.

The Priority Lane can be selected without verifying eligibility. Additionally, the existing Leave Queue action records a ticket as `no-show` rather than `left`. FR-07 addresses this distinction in Week 4.

Service management and permanent deletion, covered by FR-12 through FR-14, are planned Week 4 features rather than existing functionality.

## 1c. Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | Ticket IDs, passenger information, and ticket statuses must remain unchanged after restarting Flask and PostgreSQL without deleting the database volume. | Data reliability | Must |
| NFR-02 | Two passengers joining the queue concurrently must never receive the same ticket ID; the database must enforce unique primary keys. | Data integrity | Must |
| NFR-03 | The My Place page should load within 2 seconds under a repeatable mobile-network browser test. | Performance | Should |
| NFR-04 | The Join, My Place, and Staff pages must each achieve a Lighthouse accessibility score of at least 90. | Accessibility | Must |
| NFR-05 | Real database passwords, `.env` files, and production secret keys must not be committed to Git; this must be verified by checking tracked files and commit history. | Security | Must |
| NFR-06 | The My Place page should refresh queue status information every 10 seconds without requiring a complete page reload. | Usability | Should |

## 1d. Minimum viable product (MVP)

**MVP functional requirements:** FR-01 through FR-14.

**MVP non-functional requirements:** NFR-01, NFR-02, NFR-04, and NFR-05.

The MVP focuses on the essential baggage drop-off queue workflow. Passengers must be able to join a service lane, provide flight and baggage information, receive a ticket, monitor their queue position, and leave when necessary. Ground staff must be able to view queues, call passengers, update ticket statuses, and manage service lanes.

PostgreSQL persistence is essential because ticket information and queue status must remain available after application restarts. Unique ticket IDs are also necessary to avoid confusion when multiple passengers join the queue.

FR-15, FR-16, and FR-17 are enhancements that can be developed later. NFR-03 and NFR-06 remain additional quality targets.

### Out-of-scope features

**1. Automatic airline booking verification**

Connecting directly to airline reservation systems to validate PNRs and flight information is outside the project scope because it requires access to external airline APIs, permissions, and operational systems.

**2. Integration with airport baggage-handling equipment**

Connecting the application to physical baggage belts, check-in counter hardware, or boarding-gate systems is outside the project scope because it requires specialized equipment and airport authorization.

## 1e. Check your requirements with a real person

**Interviewee:** Airline passenger (Aveni)

**Method:** Interview

**Purpose:** To determine whether the proposed requirements address actual passenger needs and identify any missing, unnecessary, or high-priority features.

### Interview questions and responses

**Question 1: Is anything missing from the proposed requirements?**

Aveni did not identify any missing requirements. She felt that the proposed features would make NAIA ExpressPass easy to navigate once implemented.

**Question 2: Is anything wrong or unimportant?**

Aveni did not identify any incorrect or unimportant requirements.

**Question 3: Which three requirements matter most to you?**

Aveni selected the following requirements:

- **FR-02 ★:** Entering flight number, booking reference (PNR), and number of checked bags.
- **FR-03 ★:** Selecting the appropriate baggage drop-off service lane.
- **FR-11 ★:** Making flight, booking, baggage, and preferred slot information available on the staff dashboard.

### Feedback and changes

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Airline passenger | The proposed requirements would make the application easy to navigate. She found nothing missing, wrong, or unimportant. Her three highest priorities were FR-02, FR-03, and FR-11. | No requirements were changed because the passenger did not identify any missing or unnecessary features. FR-02, FR-03, and FR-11 were already classified as Must requirements, so their priorities and inclusion in the MVP were retained. |

### Decision

The interview confirmed the importance of keeping the proposed flight-information, baggage-information, and service-lane requirements.

No changes were made because the interviewee did not identify any gaps or unnecessary features. Her selection of FR-02, FR-03, and FR-11 supports their existing Must priorities and their inclusion in the minimum viable product.

