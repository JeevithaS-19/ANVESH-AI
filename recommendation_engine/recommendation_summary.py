def generate_recommendation_summary(
    result,
    education="",
    experience="",
    interests=None,
    career_goal="",
    opportunities=None
):
    """
    Generate a structured, explainable summary
    for the recommended occupation.
    """

    if interests is None:
        interests = []

    if opportunities is None:
        opportunities = []

    # -----------------------------------
    # Basic recommendation information
    # -----------------------------------

    score = result.get(
        "compatibility_score",
        0
    )

    skill_match = result.get(
        "match_percentage",
        0
    )

    career_goal_match = result.get(
        "career_goal_match",
        0
    )

    matched_skills = result.get(
        "matched_skills",
        []
    )

    missing_skills = result.get(
        "missing_skills",
        []
    )

    # -----------------------------------
    # Why this occupation was recommended
    # -----------------------------------

    reasons = []

    if skill_match >= 70:

        reasons.append(
            "Strong match with your existing skills"
        )

    elif skill_match >= 40:

        reasons.append(
            "Some of your existing skills match this occupation"
        )

    elif skill_match > 0:

        reasons.append(
            "At least one of your existing skills matches this occupation"
        )

    if education:

        reasons.append(
            "Your education was considered for this occupation"
        )

    if experience:

        reasons.append(
            "Your experience level was considered"
        )

    if interests:

        reasons.append(
            "Your interests were considered"
        )

    if career_goal_match > 0:

        reasons.append(
            "Your career goal aligns with this occupation"
        )

    # -----------------------------------
    # Skill-gap explanation
    # -----------------------------------

    skill_gaps = []

    for skill in missing_skills:

        skill_gaps.append({
            "skill": skill,
            "priority": "High",
            "reason": (
                "This skill is required for the "
                "recommended occupation"
            )
        })

    # -----------------------------------
    # Training / Next Step
    # -----------------------------------

    training = result.get(
        "training",
        []
    )

    high_priority_training = [
        item
        for item in training
        if item.get("priority") == "High"
    ]

    if high_priority_training:

        next_training = high_priority_training[0]

        next_step = (
            f"Start with {next_training['training']} "
            f"({next_training['nsqf_level']})."
        )

    elif training:

        next_training = training[0]

        next_step = (
            f"Consider {next_training['training']} "
            f"({next_training['nsqf_level']})."
        )

    elif missing_skills:

        next_step = (
            "Develop the identified skill gaps "
            "through suitable training."
        )

    else:

        next_step = (
            "You have a strong skill match. "
            "Explore suitable employment opportunities."
        )

    # -----------------------------------
    # Opportunity summary
    # -----------------------------------

    if opportunities:

        opportunity_summary = {
            "available": True,
            "count": len(opportunities),
            "message": (
                f"{len(opportunities)} relevant "
                "opportunity(ies) found."
            )
        }

    else:

        opportunity_summary = {
            "available": False,
            "count": 0,
            "message": (
                "No matching opportunity is currently "
                "available for this occupation and location."
            )
        }

    # -----------------------------------
    # Final structured response
    # -----------------------------------

    return {
        "recommended_occupation": result.get(
            "occupation",
            ""
        ),

        "compatibility_score": score,

        "skill_match": skill_match,

        "career_goal_alignment": career_goal_match,

        "why_recommended": reasons,

        "skill_gaps": skill_gaps,

        "next_step": next_step,

        "opportunity_summary": opportunity_summary
    }