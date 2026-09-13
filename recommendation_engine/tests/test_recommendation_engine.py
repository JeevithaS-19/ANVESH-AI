from recommendation_engine.recommendation_engine import generate_recommendations


user_skills = [
    "Python",
    "SQL",
    "Java"
]

results = generate_recommendations(user_skills)

print("\n===== ANVESH AI RECOMMENDATIONS =====")

for index, result in enumerate(results, start=1):
    print(f"\n{index}. {result['occupation']}")
    print(f"Skill Match: {result['skill_match']}%")
    print(f"Compatibility Score: {result['compatibility_score']}%")
    print(f"Matched Skills: {result['matched_skills']}")
    print(f"Missing Skills: {result['missing_skills']}")
    print(f"Training: {result['training']}")
    print(f"Why Recommended: {result['explanation']}")