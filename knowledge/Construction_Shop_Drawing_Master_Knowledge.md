# Construction Shop Drawing, Quantity Takeoff & IFC-Control Master Knowledge Base

**Generated:** 10 September 2026  
**Corpus:** 22 linked public/free references from the uploaded `Free Construction Shop Drawing Library` hub  
**Purpose:** persistent, machine-readable knowledge base for shop drawings, coordination, quantity takeoff (QTO), IFC compliance checking and controlled CAD editing.

## 0. Scope, evidence boundary and meaning of “zero”

This file records every structured knowledge item captured during this review. The final inclusion audit compares the knowledge-item registry against the Markdown and reaches **zero missing captured items**. “Zero” does **not** mean that every sentence in a ~22,000-page living standards corpus has been reproduced, nor that all external standards cited by UFC/UFGS (ACI, AISC, ASCE, ASTM, NFPA, ASHRAE, etc.) have been ingested. Those are explicit bounded limitations, not hidden gaps.

Two meanings of **IFC** must remain separate: **Issued for Construction drawings/documents** and **Industry Foundation Classes (.ifc) BIM files**. The source corpus primarily governs construction/design documentation; LibreCAD is a 2D CAD tool, not an IFC-BIM semantic engine.

### Authority model

For a real project, do not treat this generic corpus as automatically governing. Apply the project's document hierarchy and applicable law/code. The operational evidence chain should be: contract/conditions and project requirements → project-edited specifications → approved IFC drawings/models → approved RFIs/design changes → approved submittals/shop drawings → as-built/closeout information. A master UFGS/UFC reference explains criteria, but it cannot silently override a project-specific adopted document.

## 1. Corpus manifest and what each source actually does

| ID | Discipline | Source | Role in shop drawing/QTO workflow | Version-control finding |
|---|---|---|---|---|
| SRC-01 | All / Specifications | [UFGS Complete](https://legacy.wbdg.org/FFC/DOD/UFGS/UFGS_COMPLETE.pdf) | Master construction guide-specification corpus. Used to determine project-specific administrative, product, execution, testing and submittal requirements. | The uploaded hub labels this August 2026 (~22,099 pages). The live WBDG index is dynamic and showed a different release date/count during verification; therefore the application must version-stamp the actual downloaded file rather than trust a hard-coded label. |
| SRC-02 | Submittals | [UFGS 01 33 00 — Submittal Procedures](https://legacy.wbdg.org/FFC/DOD/UFGS/UFGS%2001%2033%2000.pdf) | Controls preparation, classification, coordination, review, variation identification, resubmission and disposition of submittals. | Use the project-edited Section 01 33 00 where available; the master is not a substitute for the contract. |
| SRC-03 | CAD / Graphics | [A/E/C Graphics Standard — Release 2.2](https://erdc-library.erdc.dren.mil/bitstream/11681/47452/1/ERDC-ITL%20SR-23-1.pdf) | Professional construction-document graphics: sheet composition, orientation, views, sections/details, symbology, linework, annotations and dimensions. | Release 2.2, August 2023. |
| SRC-04 | CAD / Data | [A/E/C CAD Standard — Release 6.2](https://erdc-library.erdc.dren.mil/bitstreams/451ab298-c17b-4154-8047-20fab3d2b4c0/download) | Nonproprietary CAD data standard covering layer/level assignments, file naming, model/sheet organization and standard symbology. | ERDC/ITL SR-24-3, July 2024. |
| SRC-05 | Structural | [UFC 3-301-01 — Structural Engineering (linked Change 4)](https://www.wbdg.org/FFC/DOD/UFC/ufc_3_301_01_2023_c4.pdf) | Structural design criteria and modifications to adopted building/structural standards; covers construction-document requirements and delegated engineered systems. | The linked Change 4 is not the latest snapshot observed during audit: WBDG also lists Change 6 dated 30 Jan 2026 and a digital UFC transition in July 2026. Version gate is mandatory. |
| SRC-06 | Architecture | [UFC 3-101-01 — Architecture (linked Change 4)](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_101_01_2020_c4.pdf) | Minimum architectural design and construction-document requirements. | Linked Change 4 dated 8 Jan 2024; WBDG digital UFC library lists an online Architecture edition from July 2026. Version gate required. |
| SRC-07 | Finishes / Tile | [UFGS 09 30 10 — Ceramic, Quarry and Glass Tiling](https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2009%2030%2010.pdf) | Tile materials, substrates, membranes, trims, grout/mortar/adhesive and execution. | Use the actual project-edited section and stamp its date. |
| SRC-08 | Finishes / Ceilings | [UFGS 09 51 00 — Acoustical Ceilings](https://www.wbdg.org/FFC/DOD/UFGS/09%2051%2000.pdf) | Acoustical units, suspension systems, hangers, access panels, colors/patterns and installation. | Master section observed with references aligned to an October 2025 UMRL; project edition governs. |
| SRC-09 | Finishes / Flooring | [UFGS 09 65 00 — Resilient Flooring](https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2009%2065%2000.pdf) | Resilient floor types, base, stair materials, mouldings, adhesives, surface preparation, testing, installation and protection. | Section dated Nov 2024 in the retrieved master; references observed aligned to Jan 2026 UMRL. |
| SRC-10 | Finishes / Coatings | [UFGS 09 90 00 — Paints and Coatings](https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2009%2090%2000.pdf) | Coating systems, qualifications, environmental constraints, product data, colors/mockups, preparation and application. | Active master; project-specific edited section governs. |
| SRC-11 | Civil / Infrastructure | [UFC 3-201-01 — Civil Engineering (linked Change 1)](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_201_01_2022_c1.pdf) | Site planning, existing conditions, grading, circulation, utilities, storm drainage and pavement/site requirements. | Linked Change 1 dated 1 Jun 2026; WBDG digital library shows a later 2026 online status/change. Version gate required. |
| SRC-12 | Wastewater | [UFC 3-240-01 — Wastewater Collection and Treatment (linked Change 4)](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_240_01_2020_c4.pdf) | Domestic/industrial wastewater collection and treatment criteria including gravity sewers, pumping/force mains and treatment. | Linked Change 4 dated 1 Oct 2024; 2026 WBDG digital/UFS transition means the latest applicable source must be checked. |
| SRC-13 | Roads / Pavement | [UFC 3-250-01 — Pavement Design for Roads and Parking Areas](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_250_01_2016.pdf) | Minimum pavement design procedures/requirements including soil investigation, flexible/rigid pavement and concrete pavement detailing concepts. | Linked PDF is dated 14 Nov 2016; WBDG lists a digital UFC 3-250-01 edition in July 2026. Treat the 2016 file as a legacy/design-detail reference unless contractually adopted. |
| SRC-14 | Road Details | [UFC 3-250-01 Road Details — Metric PDF](https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Metric.pdf) | Graphical metric details paired with pavement criteria. | Legacy companion details to the 2016 UFC. |
| SRC-15 | Road Details | [UFC 3-250-01 Road Details — Imperial PDF](https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Imperial.pdf) | English/imperial graphical companion details. | Legacy companion details to the 2016 UFC. |
| SRC-16 | Road CAD | [UFC 3-250-01 Road CADD Drawings — Metric DWG](https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Metric.dwg) | Editable CAD companion to metric pavement details. | Binary DWG was not directly inspectable in the web-analysis environment; paired official PDF was used to understand represented detail content. |
| SRC-17 | Road CAD | [UFC 3-250-01 Road CADD Drawings — Imperial DWG](https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Imperial.dwg) | Editable CAD companion to imperial pavement details. | Binary DWG not directly parsed; official paired PDF used for content understanding. |
| SRC-18 | HVAC | [UFC 3-410-01 — HVAC Systems (linked Change 1)](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_410_01_2025_c1.pdf) | HVAC design criteria; its companion UFS carries design-analysis and drawing-documentation requirements. | Linked UFC dated 28 Jul 2025, Change 1 Jan 23 2026; WBDG digital UFC library lists online UFC 3-410-01 from July 2026. |
| SRC-19 | Plumbing | [UFC 3-420-01 — Plumbing Systems](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_420_01_2021.pdf) | Plumbing design, material/equipment selection and minimum analysis/drawing requirements. | Linked PDF dated 1 Apr 2021; WBDG digital UFC library lists online UFC 3-420-01 from July 2026. |
| SRC-20 | Electrical | [UFC 3-501-01 — Electrical Engineering](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_501_01_2024.pdf) | General electrical design criteria including calculations and detailed drawing requirements. | Linked PDF dated 27 Nov 2024; WBDG digital UFC library lists online UFC 3-501-01 from July 2026. |
| SRC-21 | Fire Protection | [UFC 3-600-01 — Fire Protection Engineering for Facilities (linked Change 6)](https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_600_01_2016_c6.pdf) | Fire protection/life-safety criteria, suppression, fire alarm and coordination/commissioning requirements. | Linked UFC dated 8 Aug 2016, Change 6 May 6 2021; WBDG digital library lists online UFC 3-600-01 from July 2026. |
| SRC-22 | CAD Application | [LibreCAD Official User Manual](https://docs.librecad.org/en/latest/index.html) | Free/open-source 2D CAD operation: setup, drawing/editing, snaps, layers, blocks, dimensions/text and printing/export. | Official manual itself states it is a work in progress and may lag the latest build. |

## 2. Fundamental distinction: design criteria vs specification vs shop drawing vs CAD

**UFC** documents primarily establish design/engineering criteria and required construction-document information. **UFGS** sections establish project-editable specification requirements: administrative/submittal requirements, products and execution. **UFGS 01 33 00** controls how shop drawings and related submittals are prepared/reviewed. **A/E/C Graphics/CAD Standards** control graphical/digital structure. **LibreCAD** is a drafting application. These layers must never be collapsed into one authority.

A shop drawing is a contractor/manufacturer/fabricator-produced construction submittal showing how the work will actually be fabricated/installed and how multiple systems are coordinated. It is not a license to redesign the IFC. A proposed deviation must be detected, declared, technically evaluated and approved through the project process.

## 3. Knowledge registry — every captured learning item

| Knowledge ID | Source | Topic | Captured knowledge | Basis |
|---|---|---|---|---|
| K-001 | SRC-01 | Governance | UFGS is a living specification corpus, not a narrative textbook. Project-edited specifications govern over unedited master choices. | source-derived |
| K-002 | SRC-01 | Governance | Most technical UFGS sections follow PART 1 GENERAL, PART 2 PRODUCTS, PART 3 EXECUTION; Divisions 00/01 have formatting exceptions. | source-derived |
| K-003 | SRC-01 | Governance | The live UFGS library spans procurement/general requirements through concrete, masonry, metals, envelope, openings, finishes, fire suppression, plumbing, HVAC, electrical, earthwork, exterior improvements, utilities, transportation, process and power-generation divisions. | source-derived |
| K-004 | SRC-01 | App rule | A shop/QTO engine must bind each measured object to its project specification section, selected product/system and execution constraints rather than rely on geometry alone. | implementation inference |
| K-005 | SRC-02 | Submittals | SD-02 Shop Drawings are drawings, diagrams or schedules specifically prepared to illustrate the work, including manufacturer/fabricator information and coordination of multiple systems/interdisciplinary work. | source-derived |
| K-006 | SRC-02 | Submittals | Submittals must be complete and sufficiently detailed to demonstrate compliance; contractor QC/design review occurs before formal submission where required. | source-derived |
| K-007 | SRC-02 | Submittals | Variations/deviations from contract requirements must be clearly identified rather than hidden in a revised drawing. | source-derived |
| K-008 | SRC-02 | Submittals | Changed/revised work affecting an approved submittal requires revised submittal processing; affected work is not simply changed in the field without the required disposition. | source-derived |
| K-009 | SRC-02 | Submittals | Shop-drawing format includes drawing identification, title/number/date and revision controls; electronic PDF/native-format requirements may apply. | source-derived |
| K-010 | SRC-02 | App rule | Every generated edit should carry source IFC reference, specification reference, reason code, revision delta, responsible party and approval status. | implementation inference |
| K-011 | SRC-03 | Graphics | Good construction drawings use consistent sheet borders/title/revision areas, project orientation, view hierarchy and standardized annotation. | source-derived |
| K-012 | SRC-03 | Graphics | Plans, elevations, sections and details must use clear identifiers/callouts so references are traceable across sheets. | source-derived |
| K-013 | SRC-03 | Graphics | Linework should distinguish new/existing/demolition information and maintain legible hierarchy. | source-derived |
| K-014 | SRC-03 | Graphics | Dimensions, leaders, notes, abbreviations, legends and key plans are controlled graphical information, not decoration. | source-derived |
| K-015 | SRC-03 | App rule | Automated drawing generation should validate orphaned section/detail callouts, duplicate IDs, unreadable overlaps and contradictory dimensions before issue. | implementation inference |
| K-016 | SRC-04 | CAD | CAD levels/layers separate graphic information by discipline/function and are the basic mechanism for managing drawing data. | source-derived |
| K-017 | SRC-04 | CAD | A/E/C CAD layer names use discipline designators and major/minor groups; file naming and standard symbology are also controlled. | source-derived |
| K-018 | SRC-04 | CAD | The standard is intended to be nonproprietary and usable across platforms such as AutoCAD and MicroStation. | source-derived |
| K-019 | SRC-04 | App rule | Entity edits should preserve original layer semantics or create a controlled new layer; exploding everything into Layer 0 destroys information value. | implementation inference |
| K-020 | SRC-04 | App rule | Model-space geometry, sheet composition, external references and file names must be treated as different data objects in an automated CAD pipeline. | implementation inference |
| K-021 | SRC-05 | Structural | UFC 3-301-01 establishes structural design criteria and code modifications; it is not a complete fabrication detailing manual. | source-derived |
| K-022 | SRC-05 | Structural | Construction documents must carry required design information, including special-inspection/seismic information where applicable. | source-derived |
| K-023 | SRC-05 | Structural | Delegated engineered systems may include post-tensioning, precast/prestressed components, steel joists, specialty foundations, certain steel connections, cold-formed systems and nonstructural seismic anchorage. | source-derived |
| K-024 | SRC-05 | Structural | Delegated engineer work must be signed/sealed as required, and the Structural Engineer of Record reviews it for design intent, criteria and coordination before affected fabrication/construction. | source-derived |
| K-025 | SRC-05 | Structural | Lateral-force-resisting system connections are specifically controlled by the SER under the cited structural criteria, subject to stated exceptions. | source-derived |
| K-026 | SRC-05 | QTO | Structural takeoff must distinguish element geometry from engineering details: concrete volume can come from geometry, but reinforcement/connection quantity requires actual detailing/BBS/connection data. | implementation inference |
| K-027 | SRC-05 | Edit gate | An automatic system may correct drafting inconsistencies but must not change member sizes, reinforcement, connection design, openings or load path without engineering authority. | implementation inference |
| K-028 | SRC-06 | Architecture | Architectural final drawings require fully dimensioned floor plans with consistent orientation and cross-references. | source-derived |
| K-029 | SRC-06 | Architecture | Reflected ceiling plans must be fully coordinated with other disciplines. | source-derived |
| K-030 | SRC-06 | Architecture | Building elevations show control/expansion joints; sections/wall sections identify air, moisture and insulation barrier systems. | source-derived |
| K-031 | SRC-06 | Architecture | Door/window/louver types, schedules and details plus room finish schedule/legend/notes are part of the construction-document set. | source-derived |
| K-032 | SRC-06 | Architecture | Details should explicitly address moisture/air barrier continuity, penetrations, flashing, terminations/transitions, roof edges/parapets and drainage. | source-derived |
| K-033 | SRC-06 | Architecture | Dimensions must be sufficient to construct without unnecessary cross-sheet inference; architectural dimensions must coordinate with structural information. | source-derived |
| K-034 | SRC-06 | QTO | Architecture supports room-based and assembly-based takeoff: wall lengths/areas, floor/ceiling areas, openings, doors/windows, finishes and specialties. | implementation inference |
| K-035 | SRC-06 | Edit gate | A coordinated shop drawing can rationalize constructible layout but cannot silently change life-safety, envelope performance, opening sizes or design dimensions. | implementation inference |
| K-036 | SRC-07 | Tile | The tile specification covers tile types, mortar/adhesive/grout, substrates, trims, waterproof membranes, crack-isolation membranes, patterns and execution. | source-derived |
| K-037 | SRC-07 | Tile | Execution covers preparatory work, wall/floor tile installation, trims, expansion joints, cleaning and protection. | source-derived |
| K-038 | SRC-07 | Tile | SD-02 detail drawings and product/sample submittals are integral to the tile package. | source-derived |
| K-039 | SRC-07 | QTO | Tile QTO should separate net tile area, skirting/base, trims, transitions, membranes and joint/sealant quantities; waste is a project rule, not a hidden constant. | implementation inference |
| K-040 | SRC-07 | Edit gate | Movement joints and waterproofing/crack-isolation continuity are controlled interfaces and must not be removed for aesthetic pattern optimization. | implementation inference |
| K-041 | SRC-08 | Ceilings | The acoustical ceiling specification includes units/panels, suspension system, hangers, access panels, finishes/colors/patterns and installation. | source-derived |
| K-042 | SRC-08 | Ceilings | Shop drawings show location/extent/details of treatment, suspension system, anchoring/fastening and the reflected ceiling plan. | source-derived |
| K-043 | SRC-08 | Ceilings | Ceiling systems must coordinate lights, air terminals, access panels, penetrations and other utilities; suspension type/load capacity and seismic details matter. | source-derived |
| K-044 | SRC-08 | Ceilings | The spec warns not to suspend hanger wires/loads from the underside of steel decking in the cited execution requirement. | source-derived |
| K-045 | SRC-08 | QTO | Ceiling QTO can include panel area/count, main/cross runners, wall molding, hangers, access panels and specialty acoustic components when layout details are available. | implementation inference |
| K-046 | SRC-09 | Flooring | Resilient flooring covers multiple tile/sheet/rubber/linoleum/cork systems, wall base, stair components, mouldings, adhesives and accessories. | source-derived |
| K-047 | SRC-09 | Flooring | Drawings should show resilient flooring locations/types; execution includes substrate examination/preparation and moisture, alkalinity and bond testing. | source-derived |
| K-048 | SRC-09 | Flooring | Shop drawing and product-data submittals for resilient flooring/accessories may require Government approval as edited for the project. | source-derived |
| K-049 | SRC-09 | QTO | Flooring QTO = classified floor area plus base/transition/stair/accessory quantities; material waste must depend on module size, pattern and project rules. | implementation inference |
| K-050 | SRC-10 | Paint | Paint/coating specification covers contractor qualifications, approved products, indoor-air-quality constraints, field samples/tests, mockups, safety/environmental conditions, colors and application. | source-derived |
| K-051 | SRC-10 | Paint | Execution includes protection, surface repair/preparation and substrate-specific preparation before coating application. | source-derived |
| K-052 | SRC-10 | Paint | Paint submittals rely heavily on product data, samples/colors/mockups and tests; SD-02 is limited to specific drawing needs such as piping identification in the retrieved master. | source-derived |
| K-053 | SRC-10 | QTO | Coating QTO should be area by substrate + coating system + number/type of coats, with deductions and special surfaces governed by project measurement rules. | implementation inference |
| K-054 | SRC-11 | Civil | Civil site design must account for existing conditions, survey/geotechnical/environmental constraints, grading, vehicle circulation, parking, accessibility, utilities, stormwater and pavements. | source-derived |
| K-055 | SRC-11 | Civil | Storm drainage criteria include inlet/spread/erosion considerations, gravity systems, cover/velocity/material/outfall/structures, management facilities and pump stations. | source-derived |
| K-056 | SRC-11 | QTO | Civil QTO relies on survey/design surfaces and geometry: cut/fill, topsoil, subgrade, aggregate/asphalt/concrete, curbs, walks, drainage lines/structures and utilities. | implementation inference |
| K-057 | SRC-11 | Edit gate | Finished levels, slopes, accessible paths, storm drainage, utility offsets and road geometry require coordinated engineering checks before modification. | implementation inference |
| K-058 | SRC-12 | Wastewater | Wastewater criteria cover gravity collection, alternative sewer/pumping systems, treatment and industrial wastewater considerations. | source-derived |
| K-059 | SRC-12 | Wastewater | Gravity systems depend on hydraulic criteria, alignment/profile, minimum cover, layout and appurtenances; wastewater characteristics can constrain material selection. | source-derived |
| K-060 | SRC-12 | Wastewater | Industrial wastewater may require pretreatment/separate treatment based on pollutants and discharge requirements. | source-derived |
| K-061 | SRC-12 | QTO | Sewer QTO needs pipe length by material/diameter/slope, manholes/chambers, fittings, service connections, excavation, bedding/backfill and pumping/treatment equipment. | implementation inference |
| K-062 | SRC-12 | Edit gate | Changing a sewer route is not merely CAD editing because it can change cover, slope, inverts, hydraulic profile, crossings and pump requirements. | implementation inference |
| K-063 | SRC-13 | Roads | Pavement design is founded on soil/subgrade investigation and an approved pavement design procedure; the UFC covers flexible and rigid pavement topics. | source-derived |
| K-064 | SRC-13 | Roads | Reinforced concrete pavement can use reinforcement to address particular conditions; joint layout and odd-shaped/mismatched slabs receive specific detailing attention. | source-derived |
| K-065 | SRC-13 | QTO | Road QTO should be station/chainage aware: lengths, widths, variable layers, cut/fill, subgrade, subbase/base, asphalt/PCC, shoulders, curbs, markings, joints and drainage. | implementation inference |
| K-066 | SRC-13 | Edit gate | Horizontal/vertical alignment, crossfall, pavement thickness, joint pattern and structural reinforcement are design-controlled variables. | implementation inference |
| K-067 | SRC-14 | Road details | The visually inspected metric detail sheets include joint layouts at intersections and reinforced rigid pavement plans/sections with construction/contraction/expansion joint concepts and reinforcement/dowels. | source-derived |
| K-068 | SRC-15 | Road details | Metric and imperial companion details must be treated as equivalent concepts in different units, with explicit unit provenance. | source-derived |
| K-069 | SRC-16 | Road CAD | Official WBDG pairs the road detail PDFs with DWG CADD drawings; the DWGs provide editable vector geometry but remain standard/reference details. | source-derived |
| K-070 | SRC-17 | Road CAD | DWG content was not directly parsed in this environment; no claim is made that every native layer/block/entity was inspected. | source-derived limitation |
| K-071 | SRC-18 | HVAC | The HVAC UFC establishes design criteria; its UFS companion requires a Basis of Design and calculations demonstrating compliance. | source-derived |
| K-072 | SRC-18 | HVAC | HVAC final drawings must show equipment, ductwork and piping sufficiently to indicate installation; floor/site plans should avoid congestion and sections/elevations supplement plans. | source-derived |
| K-073 | SRC-18 | HVAC | Equipment sizing and performance documentation includes items such as terminal units, pumps, control valves/dampers, fans, AHUs, chillers, boilers and heat exchangers as applicable. | source-derived |
| K-074 | SRC-18 | QTO | HVAC takeoff should classify duct by shape/size/system/insulation, fittings separately, piping by service/diameter/material/insulation, plus valves/dampers/terminals/equipment/supports. | implementation inference |
| K-075 | SRC-18 | Edit gate | Coordination edits may change routing subject to available pressure/velocity/slope/access/fire constraints; performance and control intent remain engineering-controlled. | implementation inference |
| K-076 | SRC-19 | Plumbing | Final plumbing drawings must be accurate, to scale, and show equipment and piping sufficiently to indicate all aspects of installation. | source-derived |
| K-077 | SRC-19 | Plumbing | Plumbing documentation includes legends, seismic/ATFP bracing details, demolition separation and equipment schedules; sizing calculations support equipment and piping selections. | source-derived |
| K-078 | SRC-19 | Plumbing | Riser/equipment schedule practices support clear system topology and equipment-duty definition. | source-derived |
| K-079 | SRC-19 | QTO | Plumbing QTO should separate services (domestic cold/hot/return, sanitary, vent, storm, gas where applicable), diameter/material/insulation, fittings/valves/fixtures/equipment/supports. | implementation inference |
| K-080 | SRC-19 | Edit gate | Drainage slope/invert, pressure sizing, backflow, sanitary separation and equipment duties are engineering-controlled. | implementation inference |
| K-081 | SRC-20 | Electrical | The 2024 UFC has explicit drawing requirements for legends, site, demolition, lighting, power, telecom, grounding, roof/lightning/hazardous plans, one-lines/risers, schedules/elevations and details. | source-derived |
| K-082 | SRC-20 | Electrical | Electrical calculations cover system studies/sizing topics; drawings and calculations must remain mutually consistent. | source-derived |
| K-083 | SRC-20 | Electrical | Panelboard schedules and one-line/riser topology are structured design data, not just graphic symbols. | source-derived |
| K-084 | SRC-20 | QTO | Electrical QTO needs system/circuit semantics in addition to geometry: cable/conduit/containment lengths, conductor sizes, devices, fixtures, panels/equipment and grounding. | implementation inference |
| K-085 | SRC-20 | Edit gate | A route may be coordinated, but breaker ratings, conductor sizing, voltage drop, fault/protection coordination, hazardous areas and grounding require electrical engineering validation. | implementation inference |
| K-086 | SRC-21 | Fire | Fire protection requires specialized qualified engineering involvement for major projects across design, construction and testing/commissioning. | source-derived |
| K-087 | SRC-21 | Fire | Fire/life-safety documentation includes occupancy/egress/barrier data and coordination with structural and other disciplines. | source-derived |
| K-088 | SRC-21 | Fire | Automatic sprinkler systems use hydraulic design requirements; fire alarm systems require plans/calculations and controlled working-plan review. | source-derived |
| K-089 | SRC-21 | QTO | Fire-protection QTO should keep suppression and alarm semantics: pipe size/system, sprinklers, valves, fittings, hangers, fire pumps/tanks where applicable, alarm devices/modules/panels, wiring/conduit and interfaces. | implementation inference |
| K-090 | SRC-21 | Edit gate | Never auto-relocate life-safety devices/coverage or change hydraulic/alarm logic without code/design verification and required qualified approval. | implementation inference |
| K-091 | SRC-22 | LibreCAD | LibreCAD is a free open-source cross-platform 2D CAD application. | source-derived |
| K-092 | SRC-22 | LibreCAD | Its manual covers setup, drawing/editing, snaps, layers, blocks, dimensions/text, scales and printing/export. | source-derived |
| K-093 | SRC-22 | LibreCAD | Drawing preferences control paper, units, grid, dimensions and output; print preview supports defined scale and page layout. | source-derived |
| K-094 | SRC-22 | LibreCAD | Layers organize entities and can carry pen properties; construction layers do not print and are intended for construction geometry. | source-derived |
| K-095 | SRC-22 | LibreCAD | DXF-to-PDF conversion is available through its console tool; PDF/image/SVG outputs are supported in documented workflows. | source-derived |
| K-096 | SRC-22 | Limitation | LibreCAD is not a semantic BIM/Industry Foundation Classes engine and should not be treated as an automatic model-based QTO platform. | implementation inference |
| K-097 | SRC-01 | Cross-discipline | A construction drawing set and its specifications form one coordinated information system; neither should be interpreted in isolation. | implementation inference |
| K-098 | SRC-02 | Cross-discipline | Revision status is part of technical validity: quantity and shop-drawing decisions must always identify the drawing/spec revision used. | implementation inference |
| K-099 | SRC-03 | Cross-discipline | Plan/section/detail references provide a graph of evidence; automated extraction should traverse that graph before declaring an element complete. | implementation inference |
| K-100 | SRC-06 | Cross-discipline | The reflected ceiling is a key multidisciplinary coordination surface for architecture, HVAC, electrical and fire protection. | implementation inference |
| K-101 | SRC-05 | Cross-discipline | Structural openings/penetrations are interface-controlled; MEP routing cannot create or enlarge them without structural review when design is affected. | implementation inference |
| K-102 | SRC-11 | Cross-discipline | Civil utility coordination needs horizontal location, vertical profile, cover, clearance, crossings and connection/equipment constraints. | implementation inference |
| K-103 | SRC-18 | Cross-discipline | MEP coordination must include maintainability/access, insulation, supports, valves/dampers, equipment removal space, structure and ceiling interfaces—not only clash-free centerlines. | implementation inference |
| K-104 | SRC-21 | Cross-discipline | Fire stopping, rated barriers and life-safety penetrations must remain traceable when MEP/shop drawing routes change. | implementation inference |
| K-105 | SRC-01 | IFC workflow | For Issued-for-Construction drawings, the safe workflow is: identify governing revision → parse geometry/text/schedules → cross-check specs → resolve cross-sheet references → measure → coordinate → propose edits → classify deviation → human/engineering approval → issue revised shop drawing/QTO. | implementation inference |
| K-106 | SRC-01 | IFC workflow | For Industry Foundation Classes (.ifc) models, semantic object extraction requires BIM/IFC-capable tooling; this is outside LibreCAD's core 2D role. | implementation inference |
| K-107 | SRC-02 | IFC workflow | An edit engine needs three edit classes: drafting correction, coordination adjustment within approved design envelope, and design change/deviation. Only the first is generally safe to automate without design approval. | implementation inference |
| K-108 | SRC-02 | IFC workflow | Every quantity should carry provenance: source file, sheet/model element, revision, measurement method, unit, inclusions/exclusions and confidence/verification status. | implementation inference |
| K-109 | SRC-01 | QTO governance | A valid quantity engine must prevent double counting across plan/section/detail representations of the same physical element. | implementation inference |
| K-110 | SRC-01 | QTO governance | Quantities should be decomposed into geometry quantity, specification-derived classification, waste/allowance, and commercial measurement-rule quantity; these are not interchangeable. | implementation inference |
| K-111 | SRC-04 | CAD QA | Unit, coordinate system, drawing scale and external-reference transform must be validated before any automated CAD measurement. | implementation inference |
| K-112 | SRC-03 | CAD QA | A dimension is authoritative only within the document hierarchy and revision context; never scale a PDF pixel distance when a stated dimension/native geometry is available. | implementation inference |
| K-113 | SRC-01 | Contract hierarchy | The corpus is generic DoD criteria. On a real project, contract agreement/conditions, employer requirements, project specifications, approved IFCs, RFIs/design changes and approved submittals determine applicability and priority. | implementation inference |
| K-114 | SRC-01 | Safety/authority | A knowledge base can support checking and drafting; it does not replace the architect/engineer/qualified fire protection or other licensed/contractually responsible authority. | implementation inference |

## 4. Discipline playbooks

### 4.1 Structural

**Required inputs:** IFC structural plans/sections/details, design notes, grids/levels, schedules, structural specifications, RFIs/design changes, approved material/delegated-design submittals.

**Extract/recognize:** element IDs/types, grids/levels, member dimensions, openings/embeds, concrete grades, reinforcement marks where explicitly detailed, steel sections/connections where explicitly detailed, foundation types.

**Shop-drawing output:** general arrangements, setting-out, formwork/RC details, opening/embed coordination, delegated component drawings, connection/rebar details only where design data supports them.

**Quantity logic:** concrete m³; formwork m² by exposed faces; reinforcement kg/t only from explicit bar data/BBS or approved engineering assumptions marked as estimates; structural steel kg from member section/length and plates/bolts where detailed.

**Red-line / engineering approval gates:** member size; reinforcement; PT profile; structural opening; connection/load path; foundation; design load/seismic system.

### 4.2 Architecture & Finishes

**Required inputs:** architectural IFC plans/RCP/elevations/sections/details, room/finish/door/window schedules, UFGS Division 07-10 sections, approved samples/material submittals.

**Extract/recognize:** rooms, boundaries, wall types, openings, floor/ceiling finishes, elevations, finish extents/patterns, joints, barriers, transitions, casework/specialties.

**Shop-drawing output:** partition layouts, ceiling layouts, tile setting-out, floor pattern plans, interior elevations, finish transitions, door/window details, envelope interfaces.

**Quantity logic:** wall lengths/areas; floor/ceiling m²; tile/flooring m²; base/skirting m; doors/windows counts; paint m² by substrate/system; ceiling grid/components.

**Red-line / engineering approval gates:** life-safety dimensions; rated assemblies; envelope/air/water barrier; design joints; door egress/accessibility; approved finish/material.

### 4.3 Civil / Infrastructure

**Required inputs:** survey/DTM, site IFC, grading, utilities, drainage, profiles, geotechnical data, pavement criteria, specs, utility authority data.

**Extract/recognize:** coordinates, existing/proposed levels, contours/surfaces, alignments, slopes, drainage catchments/inlets, utility nodes/links, pavements/curbs/sidewalks.

**Shop-drawing output:** setting-out, grading details, utility plans/profiles, chambers/manholes, crossing details, road/pavement details, temporary works interfaces.

**Quantity logic:** cut/fill m³; layer volumes; pipe lengths; chambers; excavation/bedding/backfill; curbs/sidewalks/paving; drainage structures.

**Red-line / engineering approval gates:** finished levels/drainage path; road geometry; accessibility; utility hydraulic levels; clearances; authority connection points.

### 4.4 Roads

**Required inputs:** alignment/profile/cross sections, pavement design, traffic layout, drainage, survey/DTM, geotechnical, joint/detail drawings, specs.

**Extract/recognize:** chainage, centerline, widths, crossfall/superelevation, layer thickness, shoulders/medians/curbs, joints, markings, structures/drainage.

**Shop-drawing output:** setting-out, typical/variable cross sections, pavement joint layouts, kerbs/medians, tie-ins, drainage interfaces, road furniture/marking layouts.

**Quantity logic:** earthwork by station; subgrade improvement; subbase/base/asphalt/PCC volumes/tonnage; curbs; joints/dowels; markings; signs/guardrails where in scope.

**Red-line / engineering approval gates:** alignment/profile/crossfall; pavement section; joint structural design; drainage; design speed/sight distance/traffic safety.

### 4.5 HVAC

**Required inputs:** HVAC IFC plans/schematics/schedules, BOD/calculations, equipment data, ceiling/structure, fire/life-safety, controls, UFGS Division 23.

**Extract/recognize:** systems, equipment IDs/duty, ducts/pipes sizes/routes, terminals, valves/dampers, insulation, access, controls interfaces.

**Shop-drawing output:** coordinated duct/piping layouts, sections, equipment rooms, risers, details, supports, access/maintenance zones, sleeves/openings.

**Quantity logic:** duct surface/length by size, fittings, insulation, pipes by size/service, fittings/valves, terminals, equipment, supports/accessories.

**Red-line / engineering approval gates:** air/water quantities; pressure/velocity/sizing; equipment duty; smoke/fire control; control sequence; code-required clearances.

### 4.6 Plumbing

**Required inputs:** plumbing IFC, risers/schedules, calculations, fixture schedules, civil connection levels, structure/architecture, UFGS Division 22.

**Extract/recognize:** service, pipe size/material, slope/invert, fixtures, valves, cleanouts, equipment, vents, drains, insulation and supports.

**Shop-drawing output:** plans, risers, sections, congested details, equipment room layouts, sleeves/openings, hanger/support and bracing details.

**Quantity logic:** pipe length by service/size/material; fittings/valves; fixtures/equipment; insulation; supports; cleanouts/drains/accessories.

**Red-line / engineering approval gates:** sanitary slope/inverts; sizing; pressure; backflow; venting; required fixtures; equipment duty; civil tie-in.

### 4.7 Electrical

**Required inputs:** electrical IFC plans/one-lines/risers/schedules, load/short-circuit/voltage-drop/coordination studies, equipment data, architectural ceiling, UFGS Division 26.

**Extract/recognize:** system voltage, panels/equipment, circuits/feeders, containment, cable/conductor data, devices/luminaires, grounding, lightning, hazardous areas.

**Shop-drawing output:** coordinated containment layouts, lighting/power layouts, panel/equipment elevations, risers/one-lines, grounding/lightning and details.

**Quantity logic:** cable/conduit/tray lengths; conductors by size; devices; luminaires; panels/equipment; grounding; accessories/supports.

**Red-line / engineering approval gates:** one-line topology; protection; ratings; conductor sizing; panel load; grounding; hazardous classification; emergency/life safety.

### 4.8 Fire Protection

**Required inputs:** fire strategy/life-safety plans, water supply data, fire suppression/alarm IFCs, hydraulic/alarm calculations, architectural ceilings/barriers, UFGS Division 21/28.

**Extract/recognize:** hazard/occupancy, rated barriers, sprinkler/device locations, piping, valves, pumps/tanks, alarm devices/modules/panels, interfaces/cause-effect.

**Shop-drawing output:** working plans, hydraulic-calculation-linked layouts, risers, details, hangers/bracing, alarm layouts/riser/cause-effect, penetration/firestop coordination.

**Quantity logic:** sprinklers/devices; pipe/fittings/valves; pump/tank components; hangers/bracing; alarm devices/modules/panels; cable/conduit.

**Red-line / engineering approval gates:** coverage/hazard; hydraulic criteria; device spacing; egress/life safety; rated barriers; fire alarm logic; suppression system type.

### 4.9 CAD / Production

**Required inputs:** native CAD/DXF/DWG, PDFs, title blocks, Xrefs, standards, plot settings, source/issue register.

**Extract/recognize:** units, coordinates, layers, blocks, text/dimensions, sheet/view references, Xrefs, revision metadata.

**Shop-drawing output:** standard layers/naming, plans/sections/details/schedules, annotation, dimensions, title/revision data and plot output.

**Quantity logic:** measure only after units/scale/Xrefs are validated; use native vector/object data over raster scaling wherever possible.

**Red-line / engineering approval gates:** do not overwrite source; preserve revision history and distinguish graphical correction from technical design change.

## 5. Shop-drawing/submittal control model

Every submittal package should be represented as a controlled object with: project; discipline; specification section; SD category; drawing/submittal number; title; revision; source IFC drawing/model revision; related RFI/design change; manufacturer/fabricator; preparer/checker/approver; submission date; status; review comments; declared variations; superseded revision link; and issue/approval history.

A safe status flow is: **Draft → Internal Discipline Check → Multidiscipline Coordination → Contractor QC Certification → Submitted → Returned (Approved / Approved as Noted / Revise-Resubmit / Rejected or project-equivalent status) → Approved-for-Use → Superseded/As-Built**. Exact contractual statuses must be project-configurable.

### SD categories that matter

The unified submittal taxonomy includes SD-01 preconstruction, SD-02 shop drawings, SD-03 product data, SD-04 samples, SD-05 design data, SD-06 test reports, SD-07 certificates, SD-08 manufacturer instructions, SD-09 manufacturer field reports, SD-10 O&M data, plus the applicable closeout category in the current project section. Shop drawings must be read together with the related product/test/certificate data; passing only the drawing is not proof that the complete system is compliant.

## 6. Graphics and CAD production rules

The drawing generator/checker should validate: sheet number/title/revision; discipline designator; model/sheet file names; units; coordinate origin/reference; north/orientation; grid/level consistency; line hierarchy; existing/new/demolition differentiation; view/section/detail IDs; cross-references; dimensions; notes/keynotes; legends/abbreviations; schedules; title/revision blocks; Xrefs; plotted lineweights; paper size/scale; and absence of clipped/overlapping annotations.

The CAD layer model should preserve discipline and functional semantics. A layer is data, not merely color. Entity movement between layers should be recorded. Blocks should retain reusable semantics. Native model geometry should be measured directly where possible; PDF/raster scaling is a last resort and must be flagged.

## 7. IFC-to-shop-drawing workflow

1. Freeze the governing document register and revision set. 2. Ingest native CAD/BIM first, then vector PDF, then raster PDF/image as fallback. 3. Parse title blocks, grids, levels, coordinates, dimensions, schedules, notes, callouts and specification references. 4. Build a cross-sheet reference graph. 5. Create physical element/system objects and remove duplicate graphic representations. 6. Attach specification/product/execution constraints. 7. Run multidiscipline coordination. 8. Calculate quantities with provenance. 9. Generate the shop-drawing proposal. 10. Classify every change as drafting correction, coordination adjustment or design deviation. 11. Block unauthorized design changes. 12. Run drawing/CAD QA. 13. Submit through the contractual submittal workflow. 14. After disposition, issue the approved revision and update QTO/revision delta.

### Change classes

**Class A — drafting correction:** graphical/textual correction that does not change design intent, system performance, dimensions/levels or contractual scope. **Class B — coordination adjustment:** routing/setting-out adjustment within the approved design envelope; still checked for performance, access, code and interfaces. **Class C — design deviation/change:** modifies engineering/architectural intent, system performance, structural/load path, life safety, quantities/scope or specified product/system; requires the applicable design/contract approval. The application must never automatically promote Class C to “accepted.”

## 8. Quantity Takeoff data model

Each quantity record should contain `quantity_id`, `physical_element_id`, `discipline`, `system`, `work_package`, `WBS/location`, `source_file`, `source_revision`, `sheet/view/model_element`, `spec_section`, `material/product_class`, `measurement_type`, `raw_geometry_quantity`, `unit`, `deductions`, `waste_or_allowance`, `commercial_measurement_rule`, `final_quantity`, `calculation_formula`, `assumption_ids`, `confidence/verification_status`, `reviewer`, and `revision_delta`.

### Measurement principles

Use native geometry and stated dimensions ahead of scaled PDF measurement. Never double-count the same object because it appears in plan, elevation and detail. Separate **net physical quantity**, **procurement quantity including waste/packaging**, and **BOQ/payment quantity under the contract measurement rule**. Preserve metric/imperial units explicitly. Recalculate only impacted quantities after a revision and keep the before/after delta.

## 9. Discipline-specific QTO formulas and caveats


| Work item | Core calculation concept | Key caveat |
|---|---|---|
| Concrete | element volume from approved geometry | subtract openings/voids only per actual geometry/measurement rule |
| Formwork | area of formed faces | do not count faces cast against earth/blinding unless rule says otherwise |
| Reinforcement | bar length × unit mass, aggregated by mark/diameter | requires explicit bar data/BBS/detail; estimates must be labeled |
| Structural steel | section unit mass × length + plates/components | connections/bolts/coatings/fireproofing are separate |
| Walls | centerline/face length × height adjusted for openings | wall type and measurement rule control deductions |
| Plaster/paint | treated surface area by substrate/system | number of coats and exclusions are specification-driven |
| Tile/flooring | net finish area + separately measured base/trim | pattern/module/waste and transitions matter |
| Ceiling | net area plus grid/perimeter/hangers/access panels | layout and service penetrations affect component counts |
| Earthwork | existing vs proposed surface volume | survey boundaries, bulking/shrinkage and unsuitable material are separate |
| Pavement | area × layer thickness; asphalt mass = volume × approved density | variable widths/thicknesses require station/cell-based calculation |
| Pipes | 3D/plan-profile centerline length by system/size | fittings, valves, insulation, supports and wastage are separate |
| Ducts | segment length/area by size and shape | fittings, reinforcement, insulation/lining and accessories are separate |
| Cable/conduit | routed length by circuit/system | vertical drops, terminations, slack/waste and shared containment rules matter |
| Fire suppression | pipe lengths + fittings/valves/sprinklers/hangers | approved hydraulic/coverage design controls the layout |


## 10. Multidiscipline coordination matrix


| Interface | Mandatory checks |
|---|---|
| Structural ↔ Architecture | grids, levels, openings, slab edges, stairs, façade anchors, joints, wall support |
| Structural ↔ MEP | sleeves/openings, embeds, equipment loads, supports, seismic bracing, clearances |
| Architecture ↔ HVAC/Electrical/Fire | RCP module, lights, diffusers/grilles, sprinklers/detectors, access panels, signage |
| Architecture ↔ Finishes | room/finish schedule, substrate, transitions, movement joints, waterproofing, mockups |
| Civil ↔ Structural | foundation/site levels, retaining interfaces, pits/tanks, access, drainage |
| Civil ↔ Utilities | horizontal/vertical crossings, cover, chambers, connection points, protection |
| HVAC ↔ Electrical | equipment power/control, disconnects, VFDs, panels, maintenance zones |
| HVAC ↔ Fire | smoke/fire dampers, smoke control, detector/sprinkler clearances, rated penetrations |
| Plumbing ↔ Civil | incoming/outgoing connections, invert/pressure, chambers, backflow, drainage |
| All MEP ↔ Access/maintenance | valve/damper access, filter/coil removal, equipment replacement path, ceiling access |
| All penetrations ↔ Fire/Envelope | firestopping, waterproofing, air barrier, acoustic seals, corrosion protection |


## 11. What the original library does NOT fully teach by itself

The audit found important boundaries. The structural UFC references external engineering standards and does not replace detailed ACI reinforcement detailing, AISC steel detailing or specialty fabrication manuals. Fire design relies heavily on NFPA standards. HVAC relies on ASHRAE and other standards. UFGS sections cite ASTM/ANSI/AMPP/MPI and manufacturer requirements. These referenced documents may have copyright/access constraints and are outside the 22-link free corpus. Therefore this master knowledge base knows **where the boundary is** and must request/ingest project-authorized references when a decision depends on them.

The road DWG binaries were not directly parsed in this environment; the official paired PDFs and WBDG metadata were used to understand their role/content. LibreCAD is 2D and does not supply native Industry Foundation Classes semantics or automatic multidiscipline BIM clash/QTO intelligence. For `.ifc` BIM workflows, an IFC-capable parser/model environment is required in addition to this library.

## 12. Version-control findings — critical for any future application

The WBDG ecosystem changed materially in 2026: a digital UFC content library became active for multiple core/non-core UFCs. Several fixed PDFs in the original download hub therefore represent legacy/snapshot editions even though they remain highly useful references. The application must store `source_title`, `document_type`, `edition/date`, `change_number`, `retrieval_date`, `contract_adopted_revision`, and `superseded_by`; it must never assume that a filename equals the current governing criterion.

## 13. Audit logs — repeated comparison until open audit count = 0

| Log | Gaps/issues found | Open after pass | What was corrected | Definition of zero |
|---|---:|---:|---|---|
| LOG-00 Corpus inventory | 22 | 0 | Created SRC-01…SRC-22 manifest; assigned source type, shop-drawing use, QTO use, edit rule and version note. | All 22 supplied links are represented in the manifest. |
| LOG-01 Authority-role comparison | 6 | 0 | Separated design criteria, specifications, submittal governance, graphics/CAD data standards and software operation. | No source remains unclassified by authority/function. |
| LOG-02 Version drift | 9 | 0 | Added version notes and a mandatory project version gate; preserved original corpus links without silently replacing them. | No identified version discrepancy is unrecorded. |
| LOG-03 Shop-drawing governance | 8 | 0 | Integrated UFGS 01 33 00 definitions/workflow and structural delegated-design controls; created edit classes A/B/C. | No discovered shop-drawing governance concept is missing from the control model. |
| LOG-04 Discipline content | 9 | 0 | Created K-021…K-090 plus discipline playbooks covering inputs, recognition, shop outputs, QTO and approval gates. | Every discipline in the user’s table has a mapped playbook and captured knowledge items. |
| LOG-05 QTO/IFC capability | 7 | 0 | Added QTO provenance schema, measurement principles, formulas/caveats, IFC workflow and duplicate-count prevention. | No identified QTO/IFC workflow gap is unmodeled. |
| LOG-06 CAD/graphics capability | 5 | 0 | Added graphics/CAD QA, LibreCAD capabilities and CAD data preservation rules. | No discovered CAD-production rule is left uncategorized. |
| LOG-07 Cross-discipline coordination | 11 | 0 | Added K-097…K-104 and full coordination matrix. | All discovered interface categories are explicitly represented. |
| LOG-08 Known limitations | 5 | 0 | Converted each into an explicit bounded limitation/required external input instead of pretending it was learned. | No known limitation is hidden or mislabeled as knowledge. |

### Detailed audit narratives

#### LOG-00 Corpus inventory

**Detected:** 22 links had to be classified by function; the original hub grouped them by discipline but did not explain authority or applicability.

**Correction:** Created SRC-01…SRC-22 manifest; assigned source type, shop-drawing use, QTO use, edit rule and version note.

**Closure criterion:** All 22 supplied links are represented in the manifest.

#### LOG-01 Authority-role comparison

**Detected:** Risk of treating UFC design criteria, UFGS specs, shop-drawing procedures, CAD standards and LibreCAD as equivalent 'books'.

**Correction:** Separated design criteria, specifications, submittal governance, graphics/CAD data standards and software operation.

**Closure criterion:** No source remains unclassified by authority/function.

#### LOG-02 Version drift

**Detected:** Several fixed UFC PDFs are older than 2026 digital UFC entries; structural also has a later Change 6 snapshot; UFGS live index metadata is dynamic.

**Correction:** Added version notes and a mandatory project version gate; preserved original corpus links without silently replacing them.

**Closure criterion:** No identified version discrepancy is unrecorded.

#### LOG-03 Shop-drawing governance

**Detected:** Initial concept lacked full treatment of SD classifications, QC review, variations, revisions, delegated design and approval boundaries.

**Correction:** Integrated UFGS 01 33 00 definitions/workflow and structural delegated-design controls; created edit classes A/B/C.

**Closure criterion:** No discovered shop-drawing governance concept is missing from the control model.

#### LOG-04 Discipline content

**Detected:** Needed explicit operational knowledge for Structural, Architecture, Tile, Ceilings, Flooring, Paint, Civil/Wastewater/Roads, HVAC/Plumbing, Electrical/Fire.

**Correction:** Created K-021…K-090 plus discipline playbooks covering inputs, recognition, shop outputs, QTO and approval gates.

**Closure criterion:** Every discipline in the user’s table has a mapped playbook and captured knowledge items.

#### LOG-05 QTO/IFC capability

**Detected:** Books do not themselves perform QTO; risk of mixing geometric quantity, procurement waste and BOQ/payment measurement; IFC acronym ambiguity; duplicate representations.

**Correction:** Added QTO provenance schema, measurement principles, formulas/caveats, IFC workflow and duplicate-count prevention.

**Closure criterion:** No identified QTO/IFC workflow gap is unmodeled.

#### LOG-06 CAD/graphics capability

**Detected:** Needed layer/file/view semantics, units/scale/Xref validation, block/dimension handling, plotting and LibreCAD limitations.

**Correction:** Added graphics/CAD QA, LibreCAD capabilities and CAD data preservation rules.

**Closure criterion:** No discovered CAD-production rule is left uncategorized.

#### LOG-07 Cross-discipline coordination

**Detected:** Clash-free centerlines alone are insufficient; interfaces include access, supports, penetrations, ceilings, barriers, envelope, hydraulics/electrical duties and civil profiles.

**Correction:** Added K-097…K-104 and full coordination matrix.

**Closure criterion:** All discovered interface categories are explicitly represented.

#### LOG-08 Known limitations

**Detected:** External copyrighted standards not in corpus; road DWG binary not parsed; living-source version changes; project hierarchy can override; LibreCAD documentation/tooling limitations.

**Correction:** Converted each into an explicit bounded limitation/required external input instead of pretending it was learned.

**Closure criterion:** No known limitation is hidden or mislabeled as knowledge.

#### LOG-09 Markdown inclusion audit

**Detected:** Need proof that every captured K-ID and SRC-ID is actually written into the Markdown.

**Correction:** Programmatically compare registries against generated Markdown; see verification block below.

**Closure criterion:** Zero registry IDs missing from final Markdown.

## 14. Source-specific operational rules

### SRC-01 — UFGS Complete

**Role:** Master construction guide-specification corpus. Used to determine project-specific administrative, product, execution, testing and submittal requirements.

**Shop-drawing use:** Primary specification-side evidence. Query the project-edited section first; use the master only as reference.

**QTO use:** Provides material/system definitions and execution constraints; geometry/quantity normally comes from drawings/models, schedules and BOQ.

**Editing/control rule:** Never edit an IFC/shop drawing solely from a master guide-spec option. Bracketed/master choices must first be confirmed as project-selected requirements.

**Version/limitation note:** The uploaded hub labels this August 2026 (~22,099 pages). The live WBDG index is dynamic and showed a different release date/count during verification; therefore the application must version-stamp the actual downloaded file rather than trust a hard-coded label.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFGS/UFGS_COMPLETE.pdf

### SRC-02 — UFGS 01 33 00 — Submittal Procedures

**Role:** Controls preparation, classification, coordination, review, variation identification, resubmission and disposition of submittals.

**Shop-drawing use:** Defines SD-02 shop drawings and ties them to source drawings, transmittals, QC review, approval authority and variation control.

**QTO use:** Not a measurement standard; it governs the documentary status of evidence used by a quantity/shop-drawing workflow.

**Editing/control rule:** Changes/deviations must be identified and routed through the required review/approval path.

**Version/limitation note:** Use the project-edited Section 01 33 00 where available; the master is not a substitute for the contract.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFGS/UFGS%2001%2033%2000.pdf

### SRC-03 — A/E/C Graphics Standard — Release 2.2

**Role:** Professional construction-document graphics: sheet composition, orientation, views, sections/details, symbology, linework, annotations and dimensions.

**Shop-drawing use:** Controls how information is presented clearly and consistently.

**QTO use:** Improves machine/human recognition of views, dimensions, identifiers, callouts and line hierarchy but is not a takeoff method.

**Editing/control rule:** Edits should preserve graphical conventions, sheet readability and cross-references.

**Version/limitation note:** Release 2.2, August 2023.

**Source:** https://erdc-library.erdc.dren.mil/bitstream/11681/47452/1/ERDC-ITL%20SR-23-1.pdf

### SRC-04 — A/E/C CAD Standard — Release 6.2

**Role:** Nonproprietary CAD data standard covering layer/level assignments, file naming, model/sheet organization and standard symbology.

**Shop-drawing use:** Controls digital CAD structure so multi-discipline files can be exchanged and coordinated.

**QTO use:** Structured layers and names improve filtering/measurement reliability.

**Editing/control rule:** Preserve discipline designators, level/layer semantics, model/sheet separation, references and file naming.

**Version/limitation note:** ERDC/ITL SR-24-3, July 2024.

**Source:** https://erdc-library.erdc.dren.mil/bitstreams/451ab298-c17b-4154-8047-20fab3d2b4c0/download

### SRC-05 — UFC 3-301-01 — Structural Engineering (linked Change 4)

**Role:** Structural design criteria and modifications to adopted building/structural standards; covers construction-document requirements and delegated engineered systems.

**Shop-drawing use:** Defines design intent/criteria that shop drawings must respect; it is not by itself a rebar or structural-steel fabrication detailing manual.

**QTO use:** Provides system/design context; actual QTO requires geometry, reinforcement/connection data and project specifications.

**Editing/control rule:** Delegated designs require qualified engineering and SER review; do not convert an apparent drafting optimization into structural redesign.

**Version/limitation note:** The linked Change 4 is not the latest snapshot observed during audit: WBDG also lists Change 6 dated 30 Jan 2026 and a digital UFC transition in July 2026. Version gate is mandatory.

**Source:** https://www.wbdg.org/FFC/DOD/UFC/ufc_3_301_01_2023_c4.pdf

### SRC-06 — UFC 3-101-01 — Architecture (linked Change 4)

**Role:** Minimum architectural design and construction-document requirements.

**Shop-drawing use:** Defines required floor plans, RCP coordination, elevations, sections, wall types, opening schedules, finish schedules and envelope detailing.

**QTO use:** Major basis for room/finish/opening area and count extraction when drawings are sufficiently dimensioned.

**Editing/control rule:** Maintain design intent, dimensions, envelope continuity, life-safety and coordination; route design changes through approval.

**Version/limitation note:** Linked Change 4 dated 8 Jan 2024; WBDG digital UFC library lists an online Architecture edition from July 2026. Version gate required.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_101_01_2020_c4.pdf

### SRC-07 — UFGS 09 30 10 — Ceramic, Quarry and Glass Tiling

**Role:** Tile materials, substrates, membranes, trims, grout/mortar/adhesive and execution.

**Shop-drawing use:** Requires/anticipates detail drawings; shop drawings must coordinate patterns, transitions, substrates, membranes and movement joints.

**QTO use:** Supports classification of tile type, substrate, setting system, grout, trims, membranes and joint scope.

**Editing/control rule:** Do not move expansion/control joints or alter waterproofing continuity without approved design direction.

**Version/limitation note:** Use the actual project-edited section and stamp its date.

**Source:** https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2009%2030%2010.pdf

### SRC-08 — UFGS 09 51 00 — Acoustical Ceilings

**Role:** Acoustical units, suspension systems, hangers, access panels, colors/patterns and installation.

**Shop-drawing use:** Shop drawings show location/extent/details, suspension, anchoring/fastening and reflected ceiling coordination with lights, diffusers, grilles, access panels and penetrations.

**QTO use:** Enables ceiling-area, tile/panel, grid, perimeter molding, hanger/access-panel classifications when layout is available.

**Editing/control rule:** Ceiling coordination may relocate contractor-routable items only within contractual/design tolerances; protected design locations/functions require approval.

**Version/limitation note:** Master section observed with references aligned to an October 2025 UMRL; project edition governs.

**Source:** https://www.wbdg.org/FFC/DOD/UFGS/09%2051%2000.pdf

### SRC-09 — UFGS 09 65 00 — Resilient Flooring

**Role:** Resilient floor types, base, stair materials, mouldings, adhesives, surface preparation, testing, installation and protection.

**Shop-drawing use:** Shop drawings/product data must map flooring/accessory types to drawing locations and installation conditions.

**QTO use:** Floor area, base length, stair tread/riser, transition/moulding quantities plus waste can be derived from geometry when type boundaries are explicit.

**Editing/control rule:** Do not ignore moisture/alkalinity/bond requirements when selecting or changing flooring assemblies.

**Version/limitation note:** Section dated Nov 2024 in the retrieved master; references observed aligned to Jan 2026 UMRL.

**Source:** https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2009%2065%2000.pdf

### SRC-10 — UFGS 09 90 00 — Paints and Coatings

**Role:** Coating systems, qualifications, environmental constraints, product data, colors/mockups, preparation and application.

**Shop-drawing use:** Limited SD-02 need compared with other trades; product data, color samples/mockups and substrate/application controls are critical.

**QTO use:** Paint/coating QTO is primarily surface area by substrate/system/coats, with exclusions/openings defined by project rules.

**Editing/control rule:** A color or coating-system change is a controlled material/design change, not a free drafting edit.

**Version/limitation note:** Active master; project-specific edited section governs.

**Source:** https://www.wbdg.org/FFC/DOD/UFGS/UFGS%2009%2090%2000.pdf

### SRC-11 — UFC 3-201-01 — Civil Engineering (linked Change 1)

**Role:** Site planning, existing conditions, grading, circulation, utilities, storm drainage and pavement/site requirements.

**Shop-drawing use:** Provides civil design criteria behind grading, roads, parking, drainage, utility and site-development drawings.

**QTO use:** Basis for categorizing cut/fill, surfaces, pipes, structures, curbs and site features; actual quantities require survey/DTM/drawing geometry.

**Editing/control rule:** Do not alter drainage paths, finished levels, utility clearances, road geometry or accessible routes without design approval.

**Version/limitation note:** Linked Change 1 dated 1 Jun 2026; WBDG digital library shows a later 2026 online status/change. Version gate required.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_201_01_2022_c1.pdf

### SRC-12 — UFC 3-240-01 — Wastewater Collection and Treatment (linked Change 4)

**Role:** Domestic/industrial wastewater collection and treatment criteria including gravity sewers, pumping/force mains and treatment.

**Shop-drawing use:** Provides criteria behind sewer plans/profiles, manholes/appurtenances, pump stations and treatment systems.

**QTO use:** Pipe length by diameter/material, manholes, fittings, excavation, bedding, backfill, pump/equipment counts can be derived from coordinated geometry.

**Editing/control rule:** Invert elevations, gradients, hydraulic profile, capacity, pump duty and treatment process are engineering-controlled.

**Version/limitation note:** Linked Change 4 dated 1 Oct 2024; 2026 WBDG digital/UFS transition means the latest applicable source must be checked.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_240_01_2020_c4.pdf

### SRC-13 — UFC 3-250-01 — Pavement Design for Roads and Parking Areas

**Role:** Minimum pavement design procedures/requirements including soil investigation, flexible/rigid pavement and concrete pavement detailing concepts.

**Shop-drawing use:** Supports pavement layer/joint/detail interpretation; current project criteria and current UFC/UFS govern design.

**QTO use:** Layer areas/volumes, curbs, joints, dowels/tie bars and earthwork can be calculated from alignment/cross-sections/detail geometry.

**Editing/control rule:** Pavement thickness, reinforcement, joint pattern or structural section changes require design authority.

**Version/limitation note:** Linked PDF is dated 14 Nov 2016; WBDG lists a digital UFC 3-250-01 edition in July 2026. Treat the 2016 file as a legacy/design-detail reference unless contractually adopted.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_250_01_2016.pdf

### SRC-14 — UFC 3-250-01 Road Details — Metric PDF

**Role:** Graphical metric details paired with pavement criteria.

**Shop-drawing use:** Concrete pavement joint/intersection and reinforcement detail reference.

**QTO use:** Can support takeoff of joint lengths, dowel/tie-bar arrangements and detail-specific quantities when applicable.

**Editing/control rule:** Reference detail applicability must be confirmed; do not copy a standard detail into a project where geometry/criteria differ.

**Version/limitation note:** Legacy companion details to the 2016 UFC.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Metric.pdf

### SRC-15 — UFC 3-250-01 Road Details — Imperial PDF

**Role:** English/imperial graphical companion details.

**Shop-drawing use:** Same conceptual detail set in imperial units.

**QTO use:** Use only with unit-controlled conversion; never mix metric and imperial dimensions silently.

**Editing/control rule:** Unit-system provenance must remain explicit.

**Version/limitation note:** Legacy companion details to the 2016 UFC.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Imperial.pdf

### SRC-16 — UFC 3-250-01 Road CADD Drawings — Metric DWG

**Role:** Editable CAD companion to metric pavement details.

**Shop-drawing use:** Useful starting geometry/reference blocks, not project-approved shop drawings.

**QTO use:** Native vectors can improve measurement if layer/content integrity is validated.

**Editing/control rule:** Copied CAD details must be revalidated against project IFC/specification/current criteria.

**Version/limitation note:** Binary DWG was not directly inspectable in the web-analysis environment; paired official PDF was used to understand represented detail content.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Metric.dwg

### SRC-17 — UFC 3-250-01 Road CADD Drawings — Imperial DWG

**Role:** Editable CAD companion to imperial pavement details.

**Shop-drawing use:** Editable reference geometry only.

**QTO use:** Native measurement is possible after units/layers are verified.

**Editing/control rule:** Never allow automatic unit conversion without dimensional QA.

**Version/limitation note:** Binary DWG not directly parsed; official paired PDF used for content understanding.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/UFC_3-250-01_Figures_Imperial.dwg

### SRC-18 — UFC 3-410-01 — HVAC Systems (linked Change 1)

**Role:** HVAC design criteria; its companion UFS carries design-analysis and drawing-documentation requirements.

**Shop-drawing use:** Shop drawings translate design airflow/water/steam systems into coordinated routes, equipment connections, supports, access and controls while preserving design performance.

**QTO use:** Duct/pipe length by size/system, fittings, insulation, valves/dampers, terminals and equipment counts can be extracted when routes and sizes are known.

**Editing/control rule:** Routing can be coordinated; design airflow, pressure, equipment duty, fire/smoke function and control intent cannot be casually changed.

**Version/limitation note:** Linked UFC dated 28 Jul 2025, Change 1 Jan 23 2026; WBDG digital UFC library lists online UFC 3-410-01 from July 2026.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_410_01_2025_c1.pdf

### SRC-19 — UFC 3-420-01 — Plumbing Systems

**Role:** Plumbing design, material/equipment selection and minimum analysis/drawing requirements.

**Shop-drawing use:** Requires accurate scale drawings showing equipment and piping sufficiently for installation, legends, bracing details, demolition separation, risers/schedules as applicable.

**QTO use:** Pipe length by service/diameter/material; fittings, valves, fixtures, equipment, supports, insulation and drainage accessories.

**Editing/control rule:** Slope, invert, pipe sizing, fixture requirements, backflow/sanitary design and equipment duty are engineering-controlled.

**Version/limitation note:** Linked PDF dated 1 Apr 2021; WBDG digital UFC library lists online UFC 3-420-01 from July 2026.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_420_01_2021.pdf

### SRC-20 — UFC 3-501-01 — Electrical Engineering

**Role:** General electrical design criteria including calculations and detailed drawing requirements.

**Shop-drawing use:** Covers legends, site/demolition/lighting/power/telecom/grounding/roof/lightning/hazardous plans, one-lines/risers, schedules/elevations and details.

**QTO use:** Conduit/cable route lengths, devices, luminaires, panels, equipment, feeders, grounding and containment can be extracted with circuit/system semantics.

**Editing/control rule:** Circuit ratings, protection, load allocation, grounding, hazardous classification and one-line topology are design-controlled.

**Version/limitation note:** Linked PDF dated 27 Nov 2024; WBDG digital UFC library lists online UFC 3-501-01 from July 2026.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_501_01_2024.pdf

### SRC-21 — UFC 3-600-01 — Fire Protection Engineering for Facilities (linked Change 6)

**Role:** Fire protection/life-safety criteria, suppression, fire alarm and coordination/commissioning requirements.

**Shop-drawing use:** Suppression/fire-alarm working plans and calculations require qualified preparation/review; hydraulic calculations and life-safety coordination are core.

**QTO use:** Sprinklers/devices, pipe/conduit lengths/sizes, valves, fittings, hangers, alarm devices/modules/panels and specialty systems can be taken off from approved coordinated layouts.

**Editing/control rule:** Coverage, hydraulic design, egress/life-safety barriers, alarm cause/effect and suppression design are life-safety controlled.

**Version/limitation note:** Linked UFC dated 8 Aug 2016, Change 6 May 6 2021; WBDG digital library lists online UFC 3-600-01 from July 2026.

**Source:** https://legacy.wbdg.org/FFC/DOD/UFC/ufc_3_600_01_2016_c6.pdf

### SRC-22 — LibreCAD Official User Manual

**Role:** Free/open-source 2D CAD operation: setup, drawing/editing, snaps, layers, blocks, dimensions/text and printing/export.

**Shop-drawing use:** Suitable for 2D drafting/editing and DXF-based shop-drawing work.

**QTO use:** Manual/native geometric measurement is possible, but LibreCAD is not a BIM/IFC semantic quantity engine.

**Editing/control rule:** Use templates/layers/units/scale controls; preserve source provenance and issue/revision control outside the CAD editor.

**Version/limitation note:** Official manual itself states it is a work in progress and may lag the latest build.

**Source:** https://docs.librecad.org/en/latest/index.html

## 15. Machine-usable acceptance checklist

A future agent/application may claim a shop drawing or QTO package is `READY_FOR_HUMAN_APPROVAL` only when: the governing revision is known; all source sheets/views referenced by the element have been traversed; project specs are linked; units/coordinates/scale are validated; multidiscipline interfaces are checked; quantities have provenance; deviations are classified; structural/life-safety/design changes are blocked for authorized review; schedules and plans are reconciled; CAD/graphics QA passes; and every open RFI/comment affecting the work is either resolved or explicitly held.

It must never output `APPROVED` on its own. Approval is a contractual/professional authority action.

## 16. Final verification block

- Source records expected: **22**
- Source records present: **22**
- Missing source IDs: **0**
- Captured knowledge items expected: **114**
- Captured knowledge items present: **114**
- Missing knowledge IDs: **0**
- Missing source titles: **0**
- **FINAL OPEN REGISTRY/INCLUSION GAPS: 0**


### Interpretation of final zero

The final zero means **all 22 supplied sources are represented, every structured knowledge item captured in this review is written to this file, and every audit issue discovered has either been resolved in the model or explicitly converted into a bounded limitation.** It does not claim exhaustive ingestion of every word of every external standard cited by the corpus.
