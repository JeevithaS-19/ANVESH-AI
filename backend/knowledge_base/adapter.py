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
