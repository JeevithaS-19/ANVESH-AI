"""
ANVESH AI - Seed/Import Script for PostgreSQL (Member 2 / Backend)

Loads Member 5's JSON knowledge base into PostgreSQL.

Requirements:
    pip install pg8000 python-dotenv

Usage:
    python seed_import_postgres.py
"""

import json
import os

import pg8000
from dotenv import load_dotenv


# ------------------------------------------------
# Load environment variables
# ------------------------------------------------

load_dotenv()


# ------------------------------------------------
# JSON files are stored here
# ------------------------------------------------

BASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "backend",
    "knowledge_base"
)


# ------------------------------------------------
# PostgreSQL configuration
# ------------------------------------------------

PG_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "anvesh_prototype"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


# ------------------------------------------------
# Load JSON file
# ------------------------------------------------

def load(name):
    file_path = os.path.join(BASE, name)

    with open(file_path, encoding="utf-8-sig") as file:
        return json.load(file)


# ------------------------------------------------
# Main seed function
# ------------------------------------------------

def main():

    if not PG_CONFIG["password"]:
        raise ValueError(
            "POSTGRES_PASSWORD is not set in the .env file."
        )

    print("Connecting to PostgreSQL...")

    conn = None
    cur = None

    try:
        # --------------------------------------------
        # Connect to PostgreSQL
        # --------------------------------------------

        conn = pg8000.connect(**PG_CONFIG)
        cur = conn.cursor()

        print(
            f"Connected to database "
            f"'{PG_CONFIG['database']}'."
        )

        # --------------------------------------------
        # Drop old tables
        # --------------------------------------------

        cur.execute(
            """
            DROP TABLE IF EXISTS
                skills,
                occupations,
                nsqf_training,
                opportunities,
                beneficiaries_sample
            CASCADE
            """
        )

        # --------------------------------------------
        # Create skills table
        # --------------------------------------------

        cur.execute(
            """
            CREATE TABLE skills (
                skill_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                synonyms JSONB
            )
            """
        )

        # --------------------------------------------
        # Create occupations table
        # --------------------------------------------

        cur.execute(
            """
            CREATE TABLE occupations (
                occupation_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                required_skills JSONB,
                education TEXT,
                experience_level TEXT
            )
            """
        )

        # --------------------------------------------
        # Create NSQF training table
        # --------------------------------------------

        cur.execute(
            """
            CREATE TABLE nsqf_training (
                record_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                level TEXT,
                provider TEXT,
                mode TEXT,
                duration_weeks INTEGER,
                linked_skills JSONB,
                linked_occupations JSONB
            )
            """
        )

        # --------------------------------------------
        # Create opportunities table
        # --------------------------------------------

        cur.execute(
            """
            CREATE TABLE opportunities (
                opportunity_id TEXT PRIMARY KEY,
                type TEXT,
                title TEXT NOT NULL,
                location TEXT,
                linked_occupation TEXT
                    REFERENCES occupations(occupation_id)
            )
            """
        )

        # --------------------------------------------
        # Create beneficiary sample table
        # --------------------------------------------

        cur.execute(
            """
            CREATE TABLE beneficiaries_sample (
                profile_id TEXT PRIMARY KEY,
                name TEXT,
                education TEXT,
                skills JSONB,
                experience INTEGER,
                location TEXT,
                career_goal TEXT,
                job_preference TEXT,
                expected_top_match TEXT
            )
            """
        )

        print("Tables created successfully.")

        # --------------------------------------------
        # Insert skills
        # --------------------------------------------

        skills = load("skills.json")

        for skill in skills:

            cur.execute(
                """
                INSERT INTO skills (
                    skill_id,
                    name,
                    synonyms
                )
                VALUES (%s, %s, %s)
                """,
                (
                    skill["skill_id"],
                    skill["name"],
                    json.dumps(skill.get("synonyms", []))
                )
            )

        print(f"Inserted {len(skills)} skills.")

        # --------------------------------------------
        # Insert occupations
        # --------------------------------------------

        occupations = load("occupations.json")

        for occupation in occupations:

            cur.execute(
                """
                INSERT INTO occupations (
                    occupation_id,
                    name,
                    required_skills,
                    education,
                    experience_level
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    occupation["occupation_id"],
                    occupation["name"],
                    json.dumps(
                        occupation.get("required_skills", [])
                    ),
                    occupation.get("education", ""),
                    occupation.get("experience_level", "")
                )
            )

        print(
            f"Inserted {len(occupations)} occupations."
        )

        # --------------------------------------------
        # Insert NSQF training
        # --------------------------------------------

        nsqf_training = load("nsqf_training.json")

        for training in nsqf_training:

            cur.execute(
                """
                INSERT INTO nsqf_training (
                    record_id,
                    title,
                    level,
                    provider,
                    mode,
                    duration_weeks,
                    linked_skills,
                    linked_occupations
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    training["record_id"],
                    training["title"],
                    training.get("level", ""),
                    training.get("provider"),
                    training.get("mode"),
                    training.get("duration_weeks"),
                    json.dumps(
                        training.get("linked_skills", [])
                    ),
                    json.dumps(
                        training.get("linked_occupations", [])
                    )
                )
            )

        print(
            f"Inserted {len(nsqf_training)} NSQF training records."
        )

        # --------------------------------------------
        # Insert opportunities
        # --------------------------------------------

        opportunities = load("opportunities.json")

        for opportunity in opportunities:

            cur.execute(
                """
                INSERT INTO opportunities (
                    opportunity_id,
                    type,
                    title,
                    location,
                    linked_occupation
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    opportunity["opportunity_id"],
                    opportunity["type"],
                    opportunity["title"],
                    opportunity.get("location", ""),
                    opportunity["linked_occupation"]
                )
            )

        print(
            f"Inserted {len(opportunities)} opportunities."
        )

        # --------------------------------------------
        # Insert beneficiary sample data
        # --------------------------------------------

        beneficiaries = load("beneficiaries_sample.json")

        for beneficiary in beneficiaries:

            cur.execute(
                """
                INSERT INTO beneficiaries_sample (
                    profile_id,
                    name,
                    education,
                    skills,
                    experience,
                    location,
                    career_goal,
                    job_preference,
                    expected_top_match
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """,
                (
                    beneficiary["profile_id"],
                    beneficiary.get("name", ""),
                    beneficiary.get("education", ""),
                    json.dumps(
                        beneficiary.get("skills", [])
                    ),
                    beneficiary.get("experience"),
                    beneficiary.get("location", ""),
                    beneficiary.get("career_goal", ""),
                    beneficiary.get("job_preference", ""),
                    beneficiary.get("expected_top_match", "")
                )
            )

        print(
            f"Inserted {len(beneficiaries)} beneficiary samples."
        )

        # --------------------------------------------
        # Commit everything
        # --------------------------------------------

        conn.commit()

        print()
        print("PostgreSQL database seeded successfully.")
        print(
            f"Database: {PG_CONFIG['database']}"
        )

        # --------------------------------------------
        # Verify row counts
        # --------------------------------------------

        tables = [
            "skills",
            "occupations",
            "nsqf_training",
            "opportunities",
            "beneficiaries_sample"
        ]

        print()
        print("Row counts:")

        for table in tables:

            cur.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            count = cur.fetchone()[0]

            print(
                f"  {table}: {count} rows"
            )

    except Exception as error:

        if conn is not None:
            conn.rollback()

        print()
        print("ERROR while seeding PostgreSQL:")
        print(error)

        raise

    finally:

        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ------------------------------------------------
# Run script
# ------------------------------------------------


if __name__ == "__main__":
    main()