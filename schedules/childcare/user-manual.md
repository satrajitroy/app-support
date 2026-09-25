# ChildCare Schedules — User Manual

ChildCare Schedules creates childcare staff schedules locally on your iPhone. It is designed for centers that need classroom coverage plus optional coverage for breaks, lunch, prep, and other off-floor duties.

## 1. What the app does

ChildCare Schedules helps you build a weekly classroom staffing plan from:

- your center or school name,
- staff and floater / cover staff lists,
- classrooms,
- child-count demand,
- room group rules,
- staff home-room rules,
- eligibility / certification rules,
- unavailable times, and
- off-floor duties such as breaks, lunch, and prep.

The default export is compact: it includes the final classroom schedule plus Break, Lunch, and Prep columns. Full debug/audit output is available separately when needed.

## 2. Quick start

1. Open the app.
2. Use the built-in sample profile or enter your own center name.
3. Open **Staff** and choose how many teachers/core staff and floaters to use.
4. Open **Rooms** and choose how many classrooms to use.
5. Open **Child Counts** and check the demand periods.
6. Open **Breaks, Lunch & Prep** and choose whether breaks, lunch, and prep require cover.
7. Open **Create** and create the schedule.
8. Open **Results** to view, export, or share the schedule.

## 3. Staff and floaters

The app separates regular teachers/core staff from floaters/cover staff.

- **Number of teachers/core staff to use** selects from the teacher/core staff list.
- **Number of floaters to use** selects from the floater/cover staff list.

This lets you test a regular-only schedule and then explicitly add floaters without pretending that floaters are regular classroom teachers.

Example:

- 100 teachers listed
- 34 floaters listed
- Teachers/core staff to use: 70
- Floaters to use: 20
- Total selected staff: 90

## 4. Floater role

Floaters can be configured in two broad ways:

- **Cover-only**: floaters are used primarily for relief/cover duties.
- **Flexible staffing**: floaters may also be used as classroom staff when the schedule needs them.

Cover-only works best when home-room rules are on and the regular classroom staffing pattern is already meaningful. Flexible staffing works best when the scheduler may place any eligible staff member where needed.

## 5. Rooms and child counts

The room list is the set of classrooms the app may schedule. The selected room count must not exceed the listed rooms.

Child counts determine staffing demand by time period. The app uses these demand settings to decide how many staff lines are needed in each classroom/time period.

## 6. Room groups, home rooms, and eligibility

The app can use optional mapping rules:

- **Room → group map**: which classroom belongs to which age/eligibility group. The default sample treats Pre-K and School Age as separate groups because many centers staff and approve those rooms differently.
- **Staff → home room map**: each staff member’s assigned home room, if home-room rules are enabled.
- **Staff → allowed groups map**: which age/eligibility groups each staff member may work with.

The app can generate starter maps to reduce typing. These generated maps are only templates. You must review and correct them so they match your center’s real classroom groups, staff assignments, and certifications.

## 7. Unavailable times

Use unavailable-time rules when a staff member cannot work at a specific time. These are name-based restrictions. Leave them blank if everyone is available.

## 8. Breaks, lunch, prep, and cover modes

The off-class time section controls whether breaks, lunch, prep, and similar duties are treated as covered obligations.

Available modes:

- **Built-in or floater cover**: the scheduler may use surplus classroom staffing or a named floater/cover staff member.
- **Built-in staffing only**: named relief cover is disabled; the schedule succeeds only when surplus staffing already covers the room.
- **Reminders only — cover not checked**: the app records reminders but does not verify cover. This mode requires explicit confirmation and exports should be read as reminders, not as a coverage-verified schedule.

The floater capacity pre-check is a quick estimate. It helps identify clearly insufficient floater capacity before running a large search, but the final schedule still depends on the full set of constraints.

## 9. Creating a schedule

Open **Create** and run the scheduler. Large schedules can take time because the app is solving a combinatorial exact-cover problem locally on the device.

Recent phone tests show that schedules around 70 teachers across 20 classrooms can complete in minutes. In one covered-duty test without floaters, the schedule completed in about 106 seconds. With floaters and more coverage choices enabled, similar-sized runs can take around 7 minutes.

Close-to-100 staff schedules may take significantly longer, especially with covered breaks, lunch, prep, floaters, or other off-class time. Very large local runs can consume substantial memory; iOS may terminate a heavy run under memory pressure or thermal protection.

This is a phone resource warning, not a scheduler correctness warning.

## 10. Results and exports

The Results section shows each returned schedule.

The default view includes classroom assignments plus Break/Lunch/Prep columns. Use the in-app option to hide off-class columns if you want a classroom-only view. If no extra name is shown on a Break/Lunch/Prep entry, coverage is built-in staffing.

Export options may include:

- **CSV** for spreadsheet workflows,
- **PDF** for printing or sharing,
- **JSON** for structured data / integration workflows,
- **Full output** for query, raw rows, audit, and detail tables.

## 11. What “formally proven using Rocq” means

The scheduling engine is an exact-cover solver formally proven using the Rocq Prover: https://rocq-prover.org/

The Rocq proof is a soundness proof: if the app returns a schedule, the returned schedule satisfies the exact-cover rules it was given for that bounded run.

The app does not claim completeness for every bounded run. Because production runs use practical search bounds, a “no schedule found” result means no schedule was found within the configured bounds, not necessarily that no schedule exists mathematically.

## 12. Privacy and data

Scheduling is performed locally on the device. The app is intended for adult planning use and does not require login, cloud sync, ads, analytics, or a scheduling server.

Do not use the app as a place to store sensitive child records, medical records, payroll records, or confidential personnel files. Data leaves the device only when you choose to export or share it through iOS sharing features.

## 13. Troubleshooting

### No schedule found

Try reducing constraints or checking for conflicts:

- lower the number of rooms or demand lines,
- add floaters,
- widen break/lunch/prep windows,
- turn off home-room restrictions,
- check room-group and eligibility maps,
- remove impossible unavailable-time rules.

### App becomes slow or iOS closes it

The schedule may be too large for the current phone-scale run. Try reducing staff/rooms, reducing covered break/lunch/prep blocks, or running with fewer floaters.

### Export is too large

Use the compact export. Turn on full output only when you need diagnostics, raw rows, or audit information.

### A generated map looks wrong

Generated maps are starter templates, not facts. Open the map and edit it to match your center.
