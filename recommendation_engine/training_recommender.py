def normalize_text(text):
    """
    Normalize text for flexible matching.
    """
    return (
        text.lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
    )


def skill_matches_text(skill, text):
    """
    Check whether a missing skill is related to
    the supplied text.
    """

    skill = normalize_text(skill)
    text = normalize_text(text)

    # Direct match
    if skill in text:
        return True

    # Useful relationships between skills and training terms
    skill_aliases = {
        "data analysis": [
            "data analysis",
            "data analytics",
            "analytics",
            "analyst"
        ],

        "data visualization": [
            "data visualization",
            "visualization",
            "visualisation",
            "charts",
            "dashboard"
        ],

        "statistics": [
            "statistics",
            "statistical"
        ],

        "rest apis": [
            "rest api",
            "api development",
            "rest"
        ],

        "web development": [
            "web development",
            "web developer",
            "website development"
        ],

        "git/version control": [
            "git",
            "version control"
        ],

        "digital marketing": [
            "digital marketing",
            "online marketing"
        ],

        "seo": [
            "seo",
            "search engine optimization"
        ],

        "social media marketing": [
            "social media",
            "social media marketing"
        ],

        "content writing": [
            "content writing",
            "content"
        ],

        "communication skills": [
            "communication",
            "communication skills"
        ]
    }

    aliases = skill_aliases.get(skill, [])

    for alias in aliases:
        if alias in text:
            return True

    return False


def recommend_training(occupation_result, occupations):
    """
    Recommend training based on the beneficiary's
    missing skills and the occupation.

    Training receives priority when its:
    - linked skills
    - title
    - description-like text

    indicate that it can address a missing skill.
    """

    occupation_name = occupation_result["occupation"]
    missing_skills = occupation_result["missing_skills"]

    for occupation in occupations:

        if occupation["name"] != occupation_name:
            continue

        recommendations = []

        for training in occupation["training"]:

            linked_skills = training.get(
                "linked_skills",
                []
            )

            relevant_skills = []

            # ---------------------------------
            # Check linked skills from database
            # ---------------------------------

            for missing_skill in missing_skills:

                for linked_skill in linked_skills:

                    if skill_matches_text(
                        missing_skill,
                        linked_skill
                    ):
                        if missing_skill not in relevant_skills:
                            relevant_skills.append(
                                missing_skill
                            )

            # ---------------------------------
            # Also check training title
            # ---------------------------------

            training_title = training.get(
                "training",
                ""
            )

            for missing_skill in missing_skills:

                if skill_matches_text(
                    missing_skill,
                    training_title
                ):
                    if missing_skill not in relevant_skills:
                        relevant_skills.append(
                            missing_skill
                        )

            # ---------------------------------
            # Determine priority
            # ---------------------------------

            if relevant_skills:
                priority = "High"

            elif not linked_skills:
                priority = "General"

            else:
                priority = "Low"

            recommendations.append({
                "training": training["training"],
                "nsqf_level": training["nsqf_level"],
                "provider": training["provider"],
                "mode": training["mode"],
                "duration_weeks": training["duration_weeks"],
                "priority": priority,
                "relevant_missing_skills": relevant_skills
            })

        # ---------------------------------
        # High priority first
        # ---------------------------------

        priority_order = {
            "High": 0,
            "General": 1,
            "Low": 2
        }

        recommendations.sort(
            key=lambda x: (
                priority_order.get(
                    x["priority"],
                    3
                ),
                x["duration_weeks"]
            )
        )

        return {
            "occupation": occupation_name,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        }

    return {
        "occupation": occupation_name,
        "missing_skills": missing_skills,
        "recommendations": []
    }