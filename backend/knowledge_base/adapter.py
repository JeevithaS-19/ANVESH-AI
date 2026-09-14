import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_occupations():
    file_path = BASE_DIR / "occupations.json"

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_opportunities():
    file_path = BASE_DIR / "opportunities.json"

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def get_occupation_id(occupation_name):
    occupations = load_occupations()

    occupation_name = occupation_name.strip().lower()

    for occupation in occupations:
        if occupation["name"].strip().lower() == occupation_name:
            return occupation["occupation_id"]

    return None


def get_opportunities_for_occupation(occupation_name):
    occupation_id = get_occupation_id(occupation_name)

    if occupation_id is None:
        return []

    opportunities = load_opportunities()

    matched_opportunities = []

    for opportunity in opportunities:
        if opportunity["linked_occupation"] == occupation_id:
            matched_opportunities.append(opportunity)

    return matched_opportunities



def load_nsqf_training():
    file_path = BASE_DIR / "nsqf_training.json"

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def get_nsqf_training_for_occupation(occupation_name):
    occupation_id = get_occupation_id(occupation_name)

    if occupation_id is None:
        return []

    training_records = load_nsqf_training()

    matched_training = []

    for training in training_records:
        if occupation_id in training.get("linked_occupations", []):
            matched_training.append(training)

    return matched_training




def load_skills():
    file_path = BASE_DIR / "skills.json"

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def normalize_skills(user_skills):
    skills_data = load_skills()

    normalized_skills = []

    for user_skill in user_skills:
        user_skill_lower = user_skill.strip().lower()
        canonical_skill = user_skill

        for skill in skills_data:
            if user_skill_lower == skill["name"].strip().lower():
                canonical_skill = skill["name"]
                break

            for synonym in skill.get("synonyms", []):
                if user_skill_lower == synonym.strip().lower():
                    canonical_skill = skill["name"]
                    break

            if canonical_skill == skill["name"]:
                break

        if canonical_skill not in normalized_skills:
            normalized_skills.append(canonical_skill)

    return normalized_skills
