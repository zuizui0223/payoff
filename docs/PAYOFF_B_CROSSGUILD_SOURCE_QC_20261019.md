# PAYOFF-B three-guild GPS source gate

Date: 2026-10-19. Pre-data source admission; no ecology outcomes analyzed.

Selected from the all-446 Movebank census using original CC0 public datasets and independent scientific names. This is a deliberate diversity check, not representative random sampling.

| System | Data DOI | Scientific name | Original bytes | Source MD5 |
|---|---|---|---:|---|
| Taiga bean goose | 10.5441/001/1.22kk5126 | Anser fabalis | 152683274 | 1dbba0044dea9e42f69a07cdee6fb1e4 |
| Eurasian curlew | 10.5441/001/1.715k46g2 | Numenius arquata | 159155287 | b847a97e4ebaedd3e2fd46e920c4f08e |
| Steppe eagle | 10.5441/001/1.695 | Aquila nipalensis | 111170648 | eb3d377503c9d7fada00b07c9ff95675 |

Each fixed raw CC0 source is downloaded into temporary runner storage from the original Movebank repository, size/MD5 verified before opening and fully destroyed after processing. The output contains counts only, not exact locations, IDs, geospatial tracks or vital rates. For endangered eagles, sensitive positions are not reproduced.

The source screen checks original timestamp, animal/deployment/tag identifier and valid WGS84 location columns, source-year counts, identities with records in multiple years, and an outcome-blind calendar availability threshold of 10 unique dates per fixed season (winter Dec-Feb, spring Mar-May, summer Jun-Aug, autumn Sep-Nov). Months are NOT proven migration stages. Spring-autumn in same calendar year is NOT a complete migration cycle.

Crucial ecological limits: Bean goose source specifically addresses moult migration and cannot be treated as an equivalent spring breeding migration; curlew prior paper already estimated repeatable departure and wind responses; steppe eagle paper already examined age and anthropogenic decisions. None establishes a novel PAYOFF-B information use effect. Cohort independence with other PAYOFF datasets remains unverified.

The next stage requires actual departure/checkpoint dates and external cue values known before decisions, independently observed correction capacity and an identified outcome. No such test is run here.
