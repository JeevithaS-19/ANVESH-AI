from recommendation_engine.explanation import generate_explanation

result = {
    "occupation": "Data Analyst",
    "compatibility_score": 72.0,
    "matched_skills": ["Python", "SQL"],
    "missing_skills": ["Statistics"]
}

print(generate_explanation(result))