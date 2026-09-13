from recommendation_engine.occupation_matcher import rank_occupations
from recommendation_engine.training_recommender import recommend_training
from recommendation_engine.explanation import generate_explanation
from recommendation_engine.data.knowledge_base import load_knowledge_base


def generate_skill_pathway(
    missing_skills,
    training_recommendations
):
    """
    Create a personalized learning pathway
    based on the beneficiary's missing skills.
    """

    pathway = []

    for skill in missing_skills:

        pathway.append({
            "skill": skill,
            "priority": "High",
            "reason": (
                "Required skill for the "
                "recommended occupation"
            )
        })

    training_pathway = []

    for training in training_recommendations:

        training_pathway.append({
            "training": training["training"],
            "nsqf_level": training["nsqf_level"],
            "provider": training["provider"],
            "mode": training["mode"],
            "duration_weeks": training["duration_weeks"]
        })

    return {
        "skills_to_learn": pathway,
        "recommended_training": training_pathway
    }


def normalize_location(location):
    """
    Normalize location text for comparison.
    """

    if not location:
        return ""

    return (
        location
        .lower()
        .strip()
        .replace(",", "")
    )


def get_opportunities(
    occupation,
    user_location
):
    """
    Return opportunities relevant to the
    recommended occupation and beneficiary location.

    If no location is provided, all occupation-linked
    opportunities are returned.
    """

    opportunities = occupation.get(
        "opportunities",
        []
    )

    if not opportunities:
        return []

    if not user_location:
        return opportunities

    normalized_user_location = normalize_location(
        user_location
    )

    matched = []

    for opportunity in opportunities:

        opportunity_location = normalize_location(
            opportunity.get("location", "")
        )

        # Exact location match
        if opportunity_location == normalized_user_location:

            matched.append(opportunity)
            continue

        # Allow remote / all-location opportunities
        if opportunity_location in [
            "remote",
            "online",
            "all india",
            "pan india",
            "india"
        ]:

            matched.append(opportunity)

    return matched


def generate_recommendations(
    user_skills,
    education="",
    experience="",
    interests=None,
    career_goal="",
    location=""
):
    if interests is None:
        interests = []

    # Load occupations, training and opportunities
    occupations = load_knowledge_base()

    # ---------------------------------
    # Rank occupations
    # ---------------------------------

    occupation_results = rank_occupations(
        user_skills,
        occupations,
        education,
        experience,
        interests,
        career_goal
    )

    final_results = []

    for result in occupation_results:

        # ---------------------------------
        # Training recommendations
        # ---------------------------------

        training = recommend_training(
            result,
            occupations
        )

        # ---------------------------------
        # Explanation
        # ---------------------------------

        explanation = generate_explanation(
            result
        )

        # ---------------------------------
        # Personalized skill pathway
        # ---------------------------------

        skill_pathway = generate_skill_pathway(
            result["missing_skills"],
            training["recommendations"]
        )

        # ---------------------------------
        # Find matching occupation
        # ---------------------------------

        matched_occupation = None

        for occupation in occupations:

            if occupation["name"] == result["occupation"]:

                matched_occupation = occupation
                break

        # ---------------------------------
        # Opportunities
        # ---------------------------------

        opportunities = []

        if matched_occupation:

            opportunities = get_opportunities(
                matched_occupation,
                location
            )

        # ---------------------------------
        # Final result
        # ---------------------------------

        final_results.append({
            "occupation": result["occupation"],

            "skill_match": result["match_percentage"],

            "compatibility_score": (
                result["compatibility_score"]
            ),

            "matched_skills": (
                result["matched_skills"]
            ),

            "missing_skills": (
                result["missing_skills"]
            ),

            "training": (
                training["recommendations"]
            ),

            "skill_pathway": skill_pathway,

            "opportunities": opportunities,

            "explanation": explanation
        })

    # Return top 3 occupations
    return final_results[:3]