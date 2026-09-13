from recommendation_engine.skill_gap import calculate_skill_gap
from recommendation_engine.compatibility_score import calculate_compatibility_score

def match_occupation(user_skills, occupation, required_skills,
                     education_match, experience_match, interest_match):

    skill_gap = calculate_skill_gap(user_skills, required_skills)

    compatibility = calculate_compatibility_score(
        skill_gap["match_percentage"],
        education_match,
        experience_match,
        interest_match
    )

    return {
        "occupation": occupation,
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "match_percentage": skill_gap["match_percentage"],
        "compatibility_score": compatibility
    }


def rank_occupations(user_skills, occupations):
    results = []

    for occupation in occupations:
        result = match_occupation(
    user_skills,
    occupation["name"],
    occupation["required_skills"],
    occupation["education_match"],
    occupation["experience_match"],
    occupation["interest_match"]
)
        results.append(result)

    results.sort(
    key=lambda x: x["compatibility_score"],
    reverse=True
)

    return results