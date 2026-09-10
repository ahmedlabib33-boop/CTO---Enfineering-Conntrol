# ADDITIONAL LAYER — CONSTRUCTION PLANNING + PRIMAVERA P6 INTELLIGENCE

This layer is ADDED to the existing CAD + IFC + Shop Drawing + ML + Mathematics platform. Existing working modules are preserved.

## Golden data rule
PRESERVE FIRST → NORMALIZE SECOND → ANALYZE THIRD → ENGINEER FOURTH → CALCULATE FIFTH → REVIEW SIXTH → APPROVE SEVENTH → EXPORT LAST.

Raw evidence is immutable. Blanks and zeros remain distinct. Source productivity, crew, equipment, formulas and revisions are not overwritten by normalized or selected values. Unsupported values remain MISSING / UNKNOWN / UNRESOLVED / REVIEW_REQUIRED.

## Connected planning pipeline
Source Upload → Data Analyzer → Raw Evidence Vault → Normalization → Master Activity → WBS/Coding → Engineering Readiness → Procurement → Productivity → Crew → Equipment → Material → Quantity/Base Time → Duration/Man-Hour → Construction Sequence → MEP Stage → AACE 38R-06 Schedule Basis → AACE 48R-06 Constructability → Schedule QA/Conflict Gate → Engineer Decision → Primavera Schedule Builder → XER Validation → XER Creator → Controlled P6 Import → Native P6 CPM → Post-P6 QA → Final Outputs.

## Implemented functional services in V3
- deterministic duration/man-hour calculations with explicit rate-basis handling;
- backward procurement need-date analysis;
- schedule QA/open-end/relationship/calendar/duration checks;
- AACE 38R-06 schedule-basis review as guidance, not contractual mandate;
- AACE 48R-06 constructability review as guidance, not contractual mandate;
- working XER staging generator for CALENDAR / PROJECT / PROJWBS / TASK / TASKPRED;
- XER structural validation separated from schedule-quality approval;
- native Primavera P6 CPM authority warning/gate;
- planning ML task hub for activity classification, productivity, crew, duration risk, criticality risk, logic assistance, constructability risk, procurement risk and engineering-approval risk;
- anomaly detection with REVIEW_REQUIRED semantics;
- ML confidence/abstention gate;
- planning knowledge sources integrated into the persistent local knowledge index;
- Planning Intelligence web page connected to the existing UI.

## ML governance
ML recommendations remain advisory. They must not overwrite source evidence, approved Primavera logic, contract requirements, approved quantities, source rates, calendars, milestones, or P6 results. Production learning uses validated/approved labels; rejected or unreviewed predictions are not positive training truth.

## Primavera boundary
The generated XER is a staging/exchange file. Native Primavera P6 remains authoritative after import for Early/Late dates, Total/Free Float, Critical Path, Longest Path, calendar effects, constraint effects and resource-leveling effects.
