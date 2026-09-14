from recommendation_engine.data.knowledge_base import (
    load_knowledge_base
)

from recommendation_engine.occupation_matcher import (
    rank_occupations
)

from recommendation_engine.training_recommender import (
    recommend_training
)

from recommendation_engine.explanation import (
    generate_explanation
)

from recommendation_engine.recommendation_summary import (
    generate_recommendation_summary
)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

OCCUPATIONS = load_knowledge_base()


# ============================================================
# GENERATE RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    user_skills,
    education="",
    experience="",
    interests=None,
    career_goal="",
    location=""
):
    """
    Generate complete AI-based recommendations.

    Flow:
        Beneficiary Profile
              ↓
        Occupation Matching
              ↓
        Compatibility Score
              ↓
        Skill Gap
              ↓
        NSQF Training
              ↓
        Skill Pathway
              ↓
        Opportunities
              ↓
        Explainable Recommendation Summary
    """

    # --------------------------------------------------------
    # Default interests
    # --------------------------------------------------------

    if interests is None:
        interests = []

    # --------------------------------------------------------
    # STEP 1:
    # Rank occupations based on the beneficiary profile
    # --------------------------------------------------------

    occupation_results = rank_occupations(
        user_skills=user_skills,
        occupations=OCCUPATIONS,
        education=education,
        experience=experience,
        interests=interests,
        career_goal=career_goal
    )

    final_recommendations = []

    # --------------------------------------------------------
    # STEP 2:
    # Process top 3 occupations
    # --------------------------------------------------------

    for result in occupation_results[:3]:

        occupation_name = result.get(
            "occupation",
            ""
        )

        # ====================================================
        # STEP 3:
        # Recommend NSQF-aligned training
        # ====================================================

        training = recommend_training(
            result,
            OCCUPATIONS
        )

        # ====================================================
        # STEP 4:
        # Generate existing explanation
        # ====================================================

        explanation = generate_explanation(
            result
        )

        # ====================================================
        # STEP 5:
        # Create skill development pathway
        # ====================================================

        skill_pathway = []

        for skill in result.get(
            "missing_skills",
            []
        ):

            skill_pathway.append({
                "skill": skill,
                "status": "Missing",
                "action": (
                    f"Develop {skill} "
                    "through suitable training."
                )
            })

        # ====================================================
        # STEP 6:
        # Find location-aware opportunities
        # ====================================================

        opportunities = []

        for occupation in OCCUPATIONS:

            if occupation["name"] != occupation_name:
                continue

            occupation_opportunities = occupation.get(
                "opportunities",
                []
            )

            for opportunity in occupation_opportunities:

                opportunity_location = (
                    opportunity.get(
                        "location",
                        ""
                    )
                )

                # --------------------------------------------
                # If user location is not provided
                # --------------------------------------------

                if not location:

                    opportunities.append(
                        opportunity
                    )

                    continue

                # --------------------------------------------
                # Normalize locations
                # --------------------------------------------

                user_location = (
                    location
                    .lower()
                    .strip()
                )

                available_location = (
                    opportunity_location
                    .lower()
                    .strip()
                )

                # --------------------------------------------
                # Remote opportunity
                # --------------------------------------------

                if "remote" in available_location:

                    opportunities.append(
                        opportunity
                    )

                # --------------------------------------------
                # Local opportunity
                # --------------------------------------------

                elif (
                    user_location in available_location
                    or available_location in user_location
                ):

                    opportunities.append(
                        opportunity
                    )

            break

        # ====================================================
        # STEP 7:
        # Prepare result for explainable summary
        #
        # IMPORTANT:
        # The original `result` does not contain training.
        # Therefore we create a copy and attach the training
        # recommendations before generating the summary.
        # ====================================================

        summary_result = result.copy()

        summary_result["training"] = (
            training.get(
                "recommendations",
                []
            )
        )

        # ====================================================
        # STEP 8:
        # Generate structured explainable summary
        # ====================================================

        recommendation_summary = (
            generate_recommendation_summary(
                summary_result,
                education=education,
                experience=experience,
                interests=interests,
                career_goal=career_goal,
                opportunities=opportunities
            )
        )

        # ====================================================
        # STEP 9:
        # Build final recommendation object
        # ====================================================

        final_recommendations.append({

            # ------------------------------------------------
            # Occupation
            # ------------------------------------------------

            "occupation": occupation_name,

            # ------------------------------------------------
            # Scores
            # ------------------------------------------------

            "compatibility_score": result.get(
                "compatibility_score",
                0
            ),

            "match_percentage": result.get(
                "match_percentage",
                0
            ),

            "career_goal_match": result.get(
                "career_goal_match",
                0
            ),

            # ------------------------------------------------
            # Skill information
            # ------------------------------------------------

            "matched_skills": result.get(
                "matched_skills",
                []
            ),

            "missing_skills": result.get(
                "missing_skills",
                []
            ),

            # ------------------------------------------------
            # Profile matching
            # ------------------------------------------------

            "education_match": result.get(
                "education_match",
                0
            ),

            "experience_match": result.get(
                "experience_match",
                0
            ),

            "interest_match": result.get(
                "interest_match",
                0
            ),

            # ------------------------------------------------
            # Explanation
            # ------------------------------------------------

            "explanation": explanation,

            # ------------------------------------------------
            # Training recommendations
            # ------------------------------------------------

            "training": training,

            # ------------------------------------------------
            # Skill development pathway
            # ------------------------------------------------

            "skill_pathway": skill_pathway,

            # ------------------------------------------------
            # Employment / livelihood opportunities
            # ------------------------------------------------

            "opportunities": opportunities,

            # ------------------------------------------------
            # Explainable AI summary
            # ------------------------------------------------

            "recommendation_summary": (
                recommendation_summary
            )
        })

    # ========================================================
    # RETURN FINAL RECOMMENDATIONS
    # ========================================================

    return final_recommendations