# NAIA ExpressPass Schema Self-Review

## Part 3: Self-review of the schema

The NAIA ExpressPass database schema was reviewed using the six questions provided in the Week 4 activity: requirement coverage, one fact in one place, facts rather than results, prevention of bad data, delete behavior, and appropriate data types.

### Review 1 — Requirement coverage

> **Works well:** The three-table design covers the main passenger and staff tasks. Passenger information is stored in `users`, baggage-drop lane information is stored in `services`, and visit-specific information such as flight number, PNR, bag count, preferred slot, priority verification, and ticket status is stored in `tickets`.
>
> **Problem:** During the review, FR-17 was marked as storing data, but the original schema did not have a field for recording whether a passenger's Priority Lane eligibility had been verified.
>
> **Change:** I added `priority_verified` as a `boolean` column in the `tickets` table. I also updated `schema.md` and the ERD to include this field. This allows the system to store whether staff verified a passenger's eligibility for the Priority Lane.

### Review 2 — One fact in one place

> **Works well:** Each type of information has one main location. User information such as name, email, and role is stored in `users`. Service information such as the lane name, average service time, and active status is stored in `services`. Information about a passenger's specific baggage-drop visit is stored in `tickets`.
>
> **Problem:** The review checked whether information such as a passenger's email or a service's name was unnecessarily copied into `tickets`. Duplicating these values could cause inconsistent data if one copy is updated while another is not.
>
> **Change:** No schema change was needed. `tickets.user_id` references `users`, while `tickets.service_id` references `services`, so related information can be retrieved through the foreign keys instead of being duplicated.

### Review 3 — Store facts, not results

> **Works well:** The schema stores the facts required to reconstruct the queue rather than storing calculated results. `service_id`, `status`, and `created_at` can be used to determine which tickets belong to a queue and their order.
>
> **Problem:** Queue position, number of passengers ahead, estimated waiting time, and daily totals can change whenever ticket data changes. Storing these calculated values could cause them to become inconsistent with the actual ticket records.
>
> **Change:** No additional columns were added for these values. Queue position and the number of passengers ahead will be computed from active tickets for a service ordered by `created_at`. Waiting times and daily totals can also be calculated from the stored ticket information.

### Review 4 — Preventing bad data

> **Works well:** The schema uses constraints to prevent several forms of invalid data. User emails and service names are unique, `bag_count` is limited to valid values, PNR has a required length, and ticket status is restricted to the allowed status values.
>
> **Problem:** A passenger could accidentally submit the join form more than once and create multiple active tickets. Making `user_id` unique would not be appropriate because the same passenger should be allowed to create tickets on future visits.
>
> **Change:** The application will check whether the passenger already has an active `waiting` or `called` ticket before creating another ticket. Database constraints will continue to prevent invalid values for individual fields.

### Review 5 — Delete behavior

> **Works well:** The foreign keys between `tickets`, `users`, and `services` have intentional delete behavior. Tickets reference users through `user_id` and services through `service_id`.
>
> **Problem:** Automatically deleting related tickets when a user or service is deleted could remove historical queue information. Using `CASCADE` for these relationships would therefore be inappropriate.
>
> **Change:** Both foreign keys use `ON DELETE RESTRICT`. A user or service cannot be deleted while existing tickets still reference it. This also supports the requirement that a service lane can only be deleted when no tickets reference it.

### Review 6 — Appropriate data types

> **Works well:** The schema uses PostgreSQL data types that match the facts being stored. `bag_count` and `avg_minutes` use integer types, while `is_active` and the newly added `priority_verified` use boolean types. Dates and times use `timestamptz`.
>
> **Problem:** The Week 3 version accepted the passenger's preferred slot as text. Keeping a date and time as plain text in the database would make validation, comparison, and ordering more difficult.
>
> **Change:** The schema uses `preferred_slot_at` as `timestamptz`. `created_at` and `called_at` also use `timestamptz`. The application will validate and convert the preferred slot before storing it.

