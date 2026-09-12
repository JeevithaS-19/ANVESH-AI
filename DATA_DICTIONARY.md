# ANVESH AI — Knowledge Base Data Dictionary (Member 5)

Frozen field names — do not rename during the sprint. If a change is genuinely needed, raise it with M2/M4 first (per section 13 of the execution plan).

## Files
| File | Purpose |
|---|---|
| `skills.json` | 33 skills with synonyms for matching |
| `occupations.json` | 8 occupations across IT, retail, electrical, and healthcare sectors |
| `nsqf_training.json` | 10 NSQF/QP/NOS-aligned training records, each with provider/mode/duration |
| `opportunities.json` | 17 Training/Employment/Livelihood listings across 8 locations |
| `beneficiaries_sample.json` | 8 test profiles for M4 to validate the engine against |
| `seed_import.py` | Loads all JSON into `anvesh_prototype.db` (SQLite) for the prototype |
| `validate_data.py` | Checks duplicate IDs and dangling references — run after any edit |

**Note:** occupations OC006-OC008 (Retail Sales Associate, Domestic Electrician, Healthcare Support Worker) were added to demonstrate NSQF's real cross-sector range beyond IT. If the demo script only walks through IT/software examples, mention these exist in the data but weren't the focus of the walkthrough.

## Skill
| Field | Type | Notes |
|---|---|---|
| skill_id | string | e.g. `SK001`, primary key |
| name | string | canonical display name |
| synonyms | array[string] | alternate terms to match against free text/entities |

## Occupation
| Field | Type | Notes |
|---|---|---|
| occupation_id | string | e.g. `OC001`, primary key |
| name | string | display name |
| required_skills | array[skill_id] | foreign key into Skill |
| education | string | minimum education expectation |
| experience_level | string | free text range, e.g. "0-2 years" |

## NSQF/Training
| Field | Type | Notes |
|---|---|---|
| record_id | string | e.g. `TR001`, primary key |
| title | string | qualification/training name |
| level | string | NSQF level, e.g. "NSQF Level 5" |
| provider | string | training body / sector skill council name |
| mode | string | e.g. "Classroom", "Online", "Classroom + Lab" |
| duration_weeks | integer | approximate training duration |
| linked_skills | array[skill_id] | skills this training addresses |
| linked_occupations | array[occupation_id] | occupations this training feeds into |

## Opportunity
| Field | Type | Notes |
|---|---|---|
| opportunity_id | string | e.g. `OP001`, primary key |
| type | string | `Training` \| `Employment` \| `Livelihood` |
| title | string | listing title |
| location | string | city or "Remote" |
| linked_occupation | occupation_id | foreign key into Occupation |

## Beneficiary (sample/test only)
| Field | Type | Notes |
|---|---|---|
| profile_id | string | e.g. `BEN001` |
| name | string | test name |
| education | string | |
| skills | array[string] | plain skill names (matches the M3→M2 entity format) |
| experience | integer | years |
| location | string | |
| career_goal | string | |
| job_preference | string | `onsite` \| `remote` \| `hybrid` |
| expected_top_match | occupation_id | what the recommendation engine should surface — use this to sanity-check M4's output |

## Integration notes for M2
1. Run `python3 seed_import.py` to get `anvesh_prototype.db`. Swap the `sqlite3.connect()` line for your Postgres/Mongo client when ready — table/column names stay the same.
2. Every `occupation_id` referenced anywhere is guaranteed to exist in `occupations.json` — `validate_data.py` enforces this. Re-run it after any edit to the JSON files.
3. For the M2→M4 recommendation request, match the beneficiary's free-text `skills` against `skills.json` (including `synonyms`) before sending skill_ids to M4, or send plain names if M4's matching logic does the lookup — confirm which with M4 so it's not duplicated in two places.
4. Traceability guarantee: every occupation has at least one linked NSQF/training record and at least one linked opportunity, so M4's `nsqf_pathway` and `opportunities` fields will never come back empty for the 5 prototype occupations.
