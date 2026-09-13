from recommendation_engine.occupation_matcher import rank_occupations
from recommendation_engine.training_recommender import recommend_training
from recommendation_engine.explanation import generate_explanation
from recommendation_engine.data.occupations import OCCUPATIONS


def generate_recommendations(
    user_skills,
    education="",
    experience="",
    interests=None
):
    if interests is None:
        interests = []

    occupation_results = rank_occupations(
        user_skills,
        OCCUPATIONS,
        education,
        experience,
        interests
    )

    final_results = []

    for result in occupation_results:
        training = recommend_training(
            result,
            OCCUPATIONS
        )

        explanation = generate_explanation(result)

        final_results.append({
            "occupation": result["occupation"],
            "skill_match": result["match_percentage"],
            "compatibility_score": result["compatibility_score"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "training": training["recommendations"],
            "explanation": explanation
        })

    return final_results