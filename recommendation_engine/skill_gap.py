def normalize_skill(skill):
    """
    Normalize a skill name so that small differences
    in user input do not prevent matching.
    """
    return skill.strip().lower()


def calculate_skill_gap(
    user_skills,
    required_skills,
    skill_synonyms=None
):
    if skill_synonyms is None:
        skill_synonyms = {}

    # Build normalized user skill set
    user_skill_set = {
        normalize_skill(skill)
        for skill in user_skills
    }

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:

        required_normalized = normalize_skill(required_skill)

        # Direct match
        if required_normalized in user_skill_set:
            matched_skills.append(required_skill)
            continue

        # Synonym match
        synonyms = skill_synonyms.get(required_skill, [])

        synonym_match = False

        for synonym in synonyms:

            if normalize_skill(synonym) in user_skill_set:
                synonym_match = True
                break

        if synonym_match:
            matched_skills.append(required_skill)
        else:
            missing_skills.append(required_skill)

    if len(required_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100,
            2
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }