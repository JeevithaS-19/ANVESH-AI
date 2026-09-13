def calculate_skill_gap(user_skills, required_skills):
    user_skills = set(user_skills)
    required_skills = set(required_skills)

    missing_skills = required_skills - user_skills
    matched_skills = user_skills & required_skills

    if len(required_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = round((len(matched_skills) / len(required_skills)) * 100, 2)

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "match_percentage": match_percentage
    }