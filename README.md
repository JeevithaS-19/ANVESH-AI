# Member 5 — NSQF Knowledge Base & Data Lead — COMPLETE

## What's in this folder
| File | What it is |
|---|---|
| `skills.json` | 33 skills + synonyms |
| `occupations.json` | 8 occupations (IT, retail, electrical, healthcare) |
| `nsqf_training.json` | 10 NSQF/QP/NOS training records (with provider, mode, duration) |
| `opportunities.json` | 17 training/employment/livelihood listings across 8 locations |
| `beneficiaries_sample.json` | 8 test profiles with known-correct `expected_top_match` |
| `build_data.py` | Source of truth — edit this, then re-run, to change any record |
| `validate_data.py` | Integrity checker — run after every edit, must say PASSED |
| `seed_import.py` | Loads everything into `anvesh_prototype.db` for the backend |
| `anvesh_prototype.db` | Pre-seeded SQLite DB, ready for M2 to query today |
| `DATA_DICTIONARY.md` | Field-by-field reference for M2/M4 |

## How to change data safely
1. Edit `build_data.py` (never hand-edit the JSON files directly — they get overwritten).
2. `python3 build_data.py`
3. `python3 validate_data.py` — must print PASSED before you commit.
4. `python3 seed_import.py` — regenerates the DB.
5. Commit all of it together (JSON + .db stay in sync).

## Pushing to GitHub
```bash
git checkout -b member5-knowledge-base
git add skills.json occupations.json nsqf_training.json opportunities.json \
        beneficiaries_sample.json build_data.py validate_data.py seed_import.py \
        DATA_DICTIONARY.md anvesh_prototype.db
git commit -m "M5: complete NSQF knowledge base - 8 occupations, 10 training records, 17 opportunities, validated"
git push origin member5-knowledge-base
```
Then open a PR into `develop` and tag M2 + M4 for review before Integration Checkpoint 1.

## Handoff messages to send

**To M2 (Backend):**
> Knowledge base is seeded and validated. Run `python3 seed_import.py` to get `anvesh_prototype.db` — 5 tables, all foreign keys checked. Field reference is in `DATA_DICTIONARY.md`. Swap the SQLite connection for Postgres whenever you're ready; table/column names won't change.

**To M4 (Recommendation Engine):**
> `beneficiaries_sample.json` has 8 test profiles, each with an `expected_top_match` occupation_id. Run your scoring logic against all 8 — if you don't get the expected match on most of them, ping me so we figure out if it's a data gap or a scoring bug before we're both debugging blind during integration.

## 30-second jury explanation (if asked about your module)
> "I built and validated the knowledge base the recommendation engine runs on — skills, occupations, NSQF-aligned training records, and real opportunities, all cross-linked so every recommendation the AI gives can be traced back to an actual qualification and an actual opportunity, not a hallucinated one. It covers IT roles as well as retail, electrical, and healthcare, to show this works across sectors, not just tech."

## Status: all core M5 deliverables complete
- [x] Schema frozen and documented
- [x] Skills, occupations, training, opportunities datasets built
- [x] Cross-sector coverage (not just IT)
- [x] Sample beneficiary profiles with expected outcomes for M4 to test against
- [x] Referential integrity validated (zero errors)
- [x] Seed/import script working end-to-end
- [x] Data dictionary written
- [ ] Push to GitHub branch — **you need to do this from your own machine/repo access**
- [ ] Confirm with M3 that skill names match their NLP extraction output — **needs a real conversation with M3**
- [ ] Confirm with M4 that scoring logic reads `required_skills` correctly — **needs a real conversation with M4**
- [ ] Attend Integration Checkpoints 1 & 2 and Day-2 full run — **team coordination, not a data task**
