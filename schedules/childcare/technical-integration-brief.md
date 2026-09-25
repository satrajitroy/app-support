# ChildCare Schedules — Technical Integration Brief

ChildCare Schedules is an offline staff scheduling app backed by an exact-cover scheduling core formally proven using the Rocq Prover: https://rocq-prover.org/

## Exact-cover formulation

The scheduler converts childcare staffing rules into an exact-cover problem:

- Required classroom/time-period coverage cells are represented as primary constraints.
- Candidate assignments, such as assigning a staff member to a classroom, floater duty, break cover, lunch cover, or prep cover, are represented as rows.
- Availability, home-room preferences, age-group eligibility, floater rules, and off-class time are represented as compatibility constraints and row metadata.
- A valid schedule is a set of selected rows that covers the required constraints exactly while avoiding conflicts such as placing the same staff member in two places at the same time.

## Formal verification claim

In this project, “verified” means formally proven in Rocq, not merely tested on examples. Rocq is an interactive theorem prover / proof assistant used to write formal specifications, executable algorithms, and machine-checked proofs: https://rocq-prover.org/

The Rocq proof is a soundness proof for returned schedules: if the engine returns a schedule, the selected assignments satisfy the encoded exact-cover rules for that bounded run.

The app does not claim completeness for every bounded run. Because practical search fuel and bounds are used, “no schedule found” means no schedule was found within the configured bounds, not necessarily that no schedule exists mathematically.

## Device-scale behavior

Recent phone tests show that schedules around 70 teachers across 20 classrooms can complete in minutes. In one covered-duty test without floaters, the schedule completed in about 106 seconds. With floaters and more coverage choices enabled, similar-sized runs can take around 7 minutes. Close-to-100 staff schedules may take significantly longer, especially with covered breaks, lunch, prep, floaters, or other off-class time.

The reason is combinatorial: the exact-cover search space grows exponentially as more staff, rooms, time slots, coverage choices, and cover obligations are combined. Very large covered-duty runs can consume too much memory. On iPhone, iOS may terminate a heavy local run under memory pressure or thermal protection. This is a device resource limit, not a failure of the Rocq soundness proof.


## Mapping templates and user responsibility

The UI may generate starter maps such as room-to-group, staff-to-home-room, and staff-to-allowed-group maps. These are not inferred facts about the center. They are typing templates derived from the current roster, room list, group names, and simple default assumptions.

For production integrations, the host product should treat these generated maps as draft data. The operator or integrating system must supply or confirm the real mappings: classroom age/eligibility group, staff home-room assignment if used, and staff certifications or allowed age groups. The childcare sample models Pre-K and School Age as separate groups because they are often staffed and approved differently. The solver then treats the confirmed maps as constraints.

## Integration model

A childcare platform can integrate the scheduling core by mapping existing product data into a normalized scheduling problem:

- Staff roster
- Classroom roster
- Staff availability
- Classroom demand by time period
- Staff eligibility and home-room preferences
- Floater/relief staffing rules
- Break, lunch, prep, and off-floor duty policies

The engine then returns a schedule that the host platform can render, export, audit, or adjust in its own UI.
