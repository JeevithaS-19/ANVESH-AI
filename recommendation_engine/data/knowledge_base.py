import json
import sqlite3
from pathlib import Path


# Database is stored at the root of the ANVESH-AI project
DB_PATH = Path(__file__).resolve().parents[2] / "anvesh_prototype.db"


def load_knowledge_base():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # -------------------------
    # Load skills
    # -------------------------

    skill_rows = conn.execute(
        "SELECT skill_id, name, synonyms FROM skills"
    ).fetchall()

    skills = {}

    for row in skill_rows:

        skills[row["skill_id"]] = {
            "name": row["name"],
            "synonyms": json.loads(row["synonyms"] or "[]")
        }

    # -------------------------
    # Load occupations
    # -------------------------

    occupation_rows = conn.execute(
        """
        SELECT
            occupation_id,
            name,
            required_skills,
            education,
            experience_level
        FROM occupations
        """
    ).fetchall()

    occupations = []

    for row in occupation_rows:

        skill_ids = json.loads(
            row["required_skills"] or "[]"
        )

        required_skills = []
        skill_synonyms = {}

        for skill_id in skill_ids:

            if skill_id in skills:

                skill_name = skills[skill_id]["name"]

                required_skills.append(skill_name)

                skill_synonyms[skill_name] = skills[skill_id]["synonyms"]

        occupations.append({
            "occupation_id": row["occupation_id"],
            "name": row["name"],
            "required_skills": required_skills,
            "skill_synonyms": skill_synonyms,
            "education_requirements": (
                [row["education"]]
                if row["education"]
                else []
            ),
            "experience_level": row["experience_level"],
            "training": [],
            "opportunities": []
        })

    # -------------------------
    # Load NSQF training
    # -------------------------

    training_rows = conn.execute(
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
    ).fetchall()

    occupation_map = {
        occupation["occupation_id"]: occupation
        for occupation in occupations
    }

    for row in training_rows:

        linked_occupations = json.loads(
            row["linked_occupations"] or "[]"
        )

        linked_skills = json.loads(
            row["linked_skills"] or "[]"
        )

        training = {
            "training": row["title"],
            "nsqf_level": row["level"],
            "provider": row["provider"],
            "mode": row["mode"],
            "duration_weeks": row["duration_weeks"],
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

    opportunity_rows = conn.execute(
        """
        SELECT
            opportunity_id,
            type,
            title,
            location,
            linked_occupation
        FROM opportunities
        """
    ).fetchall()

    for row in opportunity_rows:

        linked_occupation = row["linked_occupation"]

        opportunity = {
            "opportunity_id": row["opportunity_id"],
            "type": row["type"],
            "title": row["title"],
            "location": row["location"]
        }

        if linked_occupation in occupation_map:

            occupation_map[
                linked_occupation
            ]["opportunities"].append(opportunity)

    conn.close()

    return occupations