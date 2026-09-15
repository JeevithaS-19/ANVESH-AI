import json
import os

import pg8000
from dotenv import load_dotenv


# Load PostgreSQL configuration from .env
load_dotenv()


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "anvesh_prototype")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

PG_CONFIG = {
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "database": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}

if POSTGRES_HOST not in ("localhost", "127.0.0.1"):
    PG_CONFIG["ssl_context"] = True


def _parse_json(value, default=None):
    """
    PostgreSQL JSON/JSONB values may be returned as strings
    or already-decoded Python objects depending on the driver.
    """
    if default is None:
        default = []

    if value is None:
        return default

    if isinstance(value, (list, dict)):
        return value

    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default

    return default


def _connect():
    """
    Create a PostgreSQL connection using the same
    environment variables used by Member 2.
    """
    if not PG_CONFIG["password"]:
        raise RuntimeError(
            "POSTGRES_PASSWORD is not set in the .env file."
        )

    return pg8000.connect(**PG_CONFIG)


def load_knowledge_base():

    conn = _connect()
    cur = conn.cursor()

    # -------------------------
    # Load skills
    # -------------------------

    cur.execute(
        """
        SELECT skill_id, name, synonyms
        FROM skills
        """
    )

    skill_rows = cur.fetchall()

    skills = {}

    for skill_id, name, synonyms in skill_rows:

        skills[skill_id] = {
            "name": name,
            "synonyms": _parse_json(synonyms, [])
        }

    # -------------------------
    # Load occupations
    # -------------------------

    cur.execute(
        """
        SELECT
            occupation_id,
            name,
            required_skills,
            education,
            experience_level
        FROM occupations
        """
    )

    occupation_rows = cur.fetchall()

    occupations = []

    for (
        occupation_id,
        name,
        required_skills_value,
        education,
        experience_level
    ) in occupation_rows:

        skill_ids = _parse_json(
            required_skills_value,
            []
        )

        required_skills = []
        skill_synonyms = {}

        for skill_id in skill_ids:

            if skill_id in skills:

                skill_name = skills[skill_id]["name"]

                required_skills.append(skill_name)

                skill_synonyms[skill_name] = (
                    skills[skill_id]["synonyms"]
                )

        occupations.append({
            "occupation_id": occupation_id,
            "name": name,
            "required_skills": required_skills,
            "skill_synonyms": skill_synonyms,
            "education_requirements": (
                [education]
                if education
                else []
            ),
            "experience_level": experience_level,
            "training": [],
            "opportunities": []
        })

    # -------------------------
    # Load NSQF training
    # -------------------------

    cur.execute(
        """
        SELECT
            record_id,
            title,
            level,
            provider,
            mode,
            duration_weeks,
            linked_skills,
            linked_occupations
        FROM nsqf_training
        """
    )

    training_rows = cur.fetchall()

    occupation_map = {
        occupation["occupation_id"]: occupation
        for occupation in occupations
    }

    for (
        record_id,
        title,
        level,
        provider,
        mode,
        duration_weeks,
        linked_skills_value,
        linked_occupations_value
    ) in training_rows:

        linked_occupations = _parse_json(
            linked_occupations_value,
            []
        )

        linked_skills = _parse_json(
            linked_skills_value,
            []
        )

        training = {
            "training": title,
            "nsqf_level": level,
            "provider": provider,
            "mode": mode,
            "duration_weeks": duration_weeks,
            "linked_skills": linked_skills
        }

        for occupation_id in linked_occupations:

            if occupation_id in occupation_map:

                occupation_map[
                    occupation_id
                ]["training"].append(training)

    # -------------------------
    # Load opportunities
    # -------------------------

    cur.execute(
        """
        SELECT
            opportunity_id,
            type,
            title,
            location,
            linked_occupation
        FROM opportunities
        """
    )

    opportunity_rows = cur.fetchall()

    for (
        opportunity_id,
        opportunity_type,
        title,
        location,
        linked_occupation
    ) in opportunity_rows:

        opportunity = {
            "opportunity_id": opportunity_id,
            "type": opportunity_type,
            "title": title,
            "location": location
        }

        if linked_occupation in occupation_map:

            occupation_map[
                linked_occupation
            ]["opportunities"].append(opportunity)

    cur.close()
    conn.close()

    return occupations