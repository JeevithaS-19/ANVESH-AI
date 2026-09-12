"""
ANVESH AI - Seed/Import Script (for Member 2 / Backend)
Loads M5's JSON knowledge base into a local SQLite database for the prototype.
Swap `sqlite3.connect(...)` for a Postgres/Mongo client later without
changing the JSON files or field names.

Usage:
    python3 seed_import.py
Produces: anvesh_prototype.db
"""
import json
import os
import sqlite3

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "anvesh_prototype.db")


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE skills (
        skill_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        synonyms TEXT
    );
    CREATE TABLE occupations (
        occupation_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        required_skills TEXT,
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
        linked_skills TEXT,
        linked_occupations TEXT
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
        skills TEXT,
        experience INTEGER,
        location TEXT,
        career_goal TEXT,
        job_preference TEXT,
        expected_top_match TEXT
    );
    """)

    for s in load("skills.json"):
        cur.execute("INSERT INTO skills VALUES (?,?,?)",
                    (s["skill_id"], s["name"], json.dumps(s["synonyms"])))

    for o in load("occupations.json"):
        cur.execute("INSERT INTO occupations VALUES (?,?,?,?,?)",
                    (o["occupation_id"], o["name"], json.dumps(o["required_skills"]),
                     o["education"], o["experience_level"]))

    for t in load("nsqf_training.json"):
        cur.execute("INSERT INTO nsqf_training VALUES (?,?,?,?,?,?,?,?)",
                    (t["record_id"], t["title"], t["level"], t.get("provider"),
                     t.get("mode"), t.get("duration_weeks"),
                     json.dumps(t["linked_skills"]), json.dumps(t["linked_occupations"])))

    for op in load("opportunities.json"):
        cur.execute("INSERT INTO opportunities VALUES (?,?,?,?,?)",
                    (op["opportunity_id"], op["type"], op["title"],
                     op["location"], op["linked_occupation"]))

    for b in load("beneficiaries_sample.json"):
        cur.execute("INSERT INTO beneficiaries_sample VALUES (?,?,?,?,?,?,?,?,?)",
                    (b["profile_id"], b["name"], b["education"], json.dumps(b["skills"]),
                     b["experience"], b["location"], b["career_goal"],
                     b["job_preference"], b["expected_top_match"]))

    conn.commit()

    counts = {}
    for table in ["skills", "occupations", "nsqf_training", "opportunities", "beneficiaries_sample"]:
        counts[table] = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    conn.close()
    print(f"Seeded {DB_PATH}:")
    for table, n in counts.items():
        print(f"  {table}: {n} rows")


if __name__ == "__main__":
    main()
