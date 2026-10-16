# Design and technology intake

Discover the user's inputs and verify compatibility before implementation.
File extensions and tutorial/internal libraries do not establish qualification.

| Material | Required review |
| --- | --- |
| Functional reference | RTL/top, parameters, includes/defines, reset behavior, specification/tests and hashes |
| Timing | Primary/generated clocks, relationships, IO delays/drivers/loads, uncertainty, exceptions, modes and unconstrained coverage |
| Logical libraries | Qualified timing models per PVT, cell functions/names and documented units |
| Physical references | Compatible technology/sites/layers and cell/macro NDM views with valid pin geometry |
| Floorplan/power/clock recipes | Authorized dimensions/density, macros/IO/blockages, supply domains, power-grid/via and clock methodology |
| Extraction | Qualified RC models/corners, layer/connectivity mappings and supported extraction recipe |
| Physical verification | Qualified DRC/LVS/antenna runsets, includes, models, mappings and authorized waiver scope |
| Stream-out | Correct top, complete cell/macro GDS, layer/datatype maps and final-stream verification methodology |
| Objectives | Explicit hard/soft timing, area, power, congestion, skew/buffer/SI goals and required IR/EM scope |

Full manifests declare qualification provenance plus technology, reference NDMs,
RC data, stream mapping/views, PG/extraction recipes and verification decks. All
paths must resolve locally. Supply required signoff corners/modes explicitly.

Ask for missing consequential requirements while continuing independent checks.
Never import a teaching example's clock or process into a user design. Missing
qualified inputs remain blockers rather than reasons to fabricate a successful flow.
