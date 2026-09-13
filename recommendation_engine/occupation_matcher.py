from recommendation_engine.skill_gap import calculate_skill_gap
from recommendation_engine.compatibility_score import calculate_compatibility_score


def calculate_text_match(user_text, required_values):
    user_text = user_text.lower()

    for value in required_values:
        if value.lower() in user_text:
            return 100

    return 0


def calculate_interest_match(user_interests, required_interests):
    user_interests = {interest.lower() for interest in user_interests}
    required_interests = {interest.lower() for interest in required_interests}

    if not required_interests:
        return 0

    matched = user_interests & required_interests

    return round(
        (len(matched) / len(required_interests)) * 100,
        2
    )


def calculate_career_goal_match(career_goal, occupation):
    if not career_goal:
        return 0

    career_goal = career_goal.lower()
    occupation = occupation.lower()

    if occupation in career_goal:
        return 100

    return 0


def match_occupation(
    user_skills,
    occupation,
    required_skills,
    education_match,
    experience_match,
    interest_match
):
    skill_gap = calculate_skill_gap(
        user_skills,
        required_skills
    )

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


def rank_occupations(
    user_skills,
    occupations,
    education="",
    experience="",
    interests=None,
    career_goal=""
):
    if interests is None:
        interests = []

    results = []

    for occupation in occupations:

        education_match = calculate_text_match(
            education,
            occupation.get("education_requirements", [])
        )

        experience_match = 100 if experience else 0

        interest_match = calculate_interest_match(
            interests,
            occupation.get("interests", [])
        )

        career_goal_match = calculate_career_goal_match(
            career_goal,
            occupation["name"]
        )

        result = match_occupation(
            user_skills,
            occupation["name"],
            occupation["required_skills"],
            education_match,
            experience_match,
            interest_match
        )

        result["career_goal_match"] = career_goal_match

        results.append(result)

    results.sort(
        key=lambda x: (
            x["career_goal_match"],
            x["compatibility_score"]
        ),
        reverse=True
    )

    return results