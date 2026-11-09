# Week 4 Validation Evidence

Validation for the NAIA ExpressPass application was tested at the browser, Flask, and PostgreSQL layers.

## Validation Tests

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Name is required and at most 120 characters | Browser | Used `required` and `maxlength="120"` on the name input | Browser prevents empty or over-length input from being submitted normally |
| Email must be valid | Browser | Used `type="email"`, `required`, and `maxlength="120"` | Browser checks email format before normal form submission |
| PNR must be exactly 6 characters | Browser | Used `minlength="6"` and `maxlength="6"` | Browser prevents normal submission of a PNR with the wrong length |
| Bag count must be between 1 and 5 | Browser | Used `type="number"`, `min="1"`, and `max="5"` | Browser prevents normal submission of values outside the allowed range |
| Email must be valid | Flask | Sent a direct `curl.exe` request with `email=not-an-email` | `HTTP/1.1 400 BAD REQUEST`; request was rejected |
| PNR must be exactly 6 characters | Flask | Sent a direct `curl.exe` request with `pnr=ABC` | `HTTP/1.1 400 BAD REQUEST`; request was rejected |
| Bag count must be between 1 and 5 | Flask | Sent a direct `curl.exe` request with `num_bags=99` | `HTTP/1.1 400 BAD REQUEST`; request was rejected |
| Service must exist and be active | Flask | Sent a direct `curl.exe` request with `service_id=99999` | `HTTP/1.1 400 BAD REQUEST`; request was rejected |
| Preferred slot must be allowed | Flask | Sent a direct `curl.exe` request with `slot_time=INVALID` | `HTTP/1.1 400 BAD REQUEST`; request was rejected |
| Bag count must be between 1 and 5 | Database — CHECK | Inserted a ticket with `bag_count=99` in psql | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_bag_count"` |
| PNR must be exactly 6 characters | Database — CHECK | Inserted a ticket with `pnr='ABC'` in psql | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_pnr_length"` |
| Ticket status must be an allowed value | Database — CHECK | Inserted a ticket with `status='hacked'` in psql | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Service referenced by a ticket must exist | Database — FOREIGN KEY | Inserted a ticket with `service_id=999` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Service names must be unique | Database — UNIQUE | Inserted another service named `Priority Lane (OFW / Senior / PWD / Infant)` | `ERROR: duplicate key value violates unique constraint "services_name_key"` |
| Service name cannot be NULL | Database — NOT NULL | Inserted a service with `name=NULL` | `ERROR: null value in column "name" of relation "services" violates not-null constraint` |
| Referenced service cannot be deleted | Database — RESTRICT | Tried to delete service `id=2`, which was referenced by a ticket | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |

## Flask Validation Test

Browser validation was bypassed by sending invalid values directly to the Flask application:

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/join `
  -d "name=Test User" `
  -d "email=not-an-email" `
  -d "flight_number=THIS-FLIGHT-NUMBER-IS-WAY-TOO-LONG" `
  -d "pnr=ABC" `
  -d "num_bags=99" `
  -d "service_id=99999" `
  -d "slot_time=INVALID"