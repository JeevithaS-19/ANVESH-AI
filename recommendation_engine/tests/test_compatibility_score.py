from recommendation_engine.compatibility_score import calculate_compatibility_score

score = calculate_compatibility_score(
    skill_match=80,
    education_match=100,
    experience_match=60,
    interest_match=90
)

print("Compatibility Score:", score)