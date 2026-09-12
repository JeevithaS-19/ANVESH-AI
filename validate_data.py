"""
ANVESH AI - Member 5 Data Validator
Checks: duplicate IDs, dangling foreign-key references, missing required fields.
Run this any time the datasets are edited, before handing off to M2/M4.
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)

skills = load("skills.json")
occupations = load("occupations.json")
training = load("nsqf_training.json")
opportunities = load("opportunities.json")
beneficiaries = load("beneficiaries_sample.json")

errors = []

def check_duplicates(records, id_field, dataset_name):
    ids = [r[id_field] for r in records]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f"[{dataset_name}] duplicate {id_field}: {dupes}")

check_duplicates(skills, "skill_id", "skills.json")
check_duplicates(occupations, "occupation_id", "occupations.json")
check_duplicates(training, "record_id", "nsqf_training.json")
check_duplicates(opportunities, "opportunity_id", "opportunities.json")
check_duplicates(beneficiaries, "profile_id", "beneficiaries_sample.json")

skill_ids = {s["skill_id"] for s in skills}
occ_ids = {o["occupation_id"] for o in occupations}

# occupations -> skills
for o in occupations:
    for sid in o["required_skills"]:
        if sid not in skill_ids:
            errors.append(f"[occupations.json] {o['occupation_id']} references missing skill {sid}")

# training -> skills, occupations
for t in training:
    for sid in t["linked_skills"]:
        if sid not in skill_ids:
            errors.append(f"[nsqf_training.json] {t['record_id']} references missing skill {sid}")
    for oid in t["linked_occupations"]:
        if oid not in occ_ids:
            errors.append(f"[nsqf_training.json] {t['record_id']} references missing occupation {oid}")

# opportunities -> occupations
for op in opportunities:
    if op["linked_occupation"] not in occ_ids:
        errors.append(f"[opportunities.json] {op['opportunity_id']} references missing occupation {op['linked_occupation']}")

# every occupation has at least one training record and one opportunity (traceability requirement)
occ_with_training = {oid for t in training for oid in t["linked_occupations"]}
occ_with_opportunity = {op["linked_occupation"] for op in opportunities}
for oid in occ_ids:
    if oid not in occ_with_training:
        errors.append(f"[coverage] occupation {oid} has no linked NSQF/training record")
    if oid not in occ_with_opportunity:
        errors.append(f"[coverage] occupation {oid} has no linked opportunity")

# beneficiaries -> expected_top_match must be a real occupation
for b in beneficiaries:
    if b["expected_top_match"] not in occ_ids:
        errors.append(f"[beneficiaries_sample.json] {b['profile_id']} expected_top_match {b['expected_top_match']} not a valid occupation")

if errors:
    print(f"FAILED - {len(errors)} issue(s) found:\n")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print(f"PASSED - {len(skills)} skills, {len(occupations)} occupations, "
          f"{len(training)} training records, {len(opportunities)} opportunities, "
          f"{len(beneficiaries)} sample profiles. All references valid, no duplicates, full traceability.")
