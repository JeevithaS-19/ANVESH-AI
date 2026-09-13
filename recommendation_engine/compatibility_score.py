def calculate_compatibility_score(
    skill_match,
    education_match,
    experience_match,
    interest_match
):
    score = (
        skill_match * 0.60 +
        education_match * 0.15 +
        experience_match * 0.15 +
        interest_match * 0.10
    )

    return round(score, 2)