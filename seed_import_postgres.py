"""
ANVESH AI - Seed/Import Script for PostgreSQL (for Member 2 / Backend)
Loads M5's JSON knowledge base into PostgreSQL.
Identical table/column names to the SQLite version - only the
connection + a couple of Postgres-specific syntax tweaks changed.

Requires: pip install psycopg2-binary
Usage:
    python3 seed_import_postgres.py
"""
import json
import os
import psycopg2

BASE = os.path.dirname(os.path.abspath(__file__))

# Update these to match your actual Postgres setup (or read from env vars)
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "anvesh_prototype",
    "user": "postgres",
    "password": "postgres",
}


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE IF EXISTS skills, occupations, nsqf_training, opportunities, beneficiaries_sample CASCADE;

    CREATE TABLE skills (
        skill_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        synonyms JSONB
    );
    CREATE TABLE occupations (
        occupation_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        required_skills JSONB,
        education TEXT,
        experience_level TEXT
    );
    CREATE TABLE nsqf_training (
        record_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        level TEXT,
        provider TEXT,
        mode TEXT,
        duration_weeks INTEGER,
        linked_skills JSONB,
        linked_occupations JSONB
    );
    CREATE TABLE opportunities (
        opportunity_id TEXT PRIMARY KEY,
        type TEXT,
        title TEXT NOT NULL,
        location TEXT,
        linked_occupation TEXT REFERENCES occupations(occupation_id)
    );
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
    );
    """)

    for s in load("skills.json"):
        cur.execute("INSERT INTO skills VALUES (%s,%s,%s)",
                    (s["skill_id"], s["name"], json.dumps(s["synonyms"])))

    for o in load("occupations.json"):
        cur.execute("INSERT INTO occupations VALUES (%s,%s,%s,%s,%s)",
                    (o["occupation_id"], o["name"], json.dumps(o["required_skills"]),
                     o["education"], o["experience_level"]))

    for t in load("nsqf_training.json"):
        cur.execute("INSERT INTO nsqf_training VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (t["record_id"], t["title"], t["level"], t.get("provider"),
                     t.get("mode"), t.get("duration_weeks"),
                     json.dumps(t["linked_skills"]), json.dumps(t["linked_occupations"])))

    for op in load("opportunities.json"):
        cur.execute("INSERT INTO opportunities VALUES (%s,%s,%s,%s,%s)",
                    (op["opportunity_id"], op["type"], op["title"],
                     op["location"], op["linked_occupation"]))

    for b in load("beneficiaries_sample.json"):
        cur.execute("INSERT INTO beneficiaries_sample VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (b["profile_id"], b["name"], b["education"], json.dumps(b["skills"]),
                     b["experience"], b["location"], b["career_goal"],
                     b["job_preference"], b["expected_top_match"]))

    conn.commit()

    counts = {}
    for table in ["skills", "occupations", "nsqf_training", "opportunities", "beneficiaries_sample"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cur.fetchone()[0]

    cur.close()
    conn.close()
    print(f"Seeded PostgreSQL database '{PG_CONFIG['dbname']}':")
    for table, n in counts.items():
        print(f"  {table}: {n} rows")


if __name__ == "__main__":
    main()
