from recommendation_engine.training_recommender import recommend_training
from recommendation_engine.occupation_matcher import rank_occupations
from recommendation_engine.data.occupations import OCCUPATIONS

user_skills = ["Python", "SQL", "Java"]

results = rank_occupations(user_skills, OCCUPATIONS)

for result in results:
    recommendation = recommend_training(result, OCCUPATIONS)

    print("\nOccupation:", recommendation["occupation"])
    print("Missing Skills:", recommendation["missing_skills"])
    print("Training Recommendations:")

    for training in recommendation["recommendations"]:
        print(
            training["training"],
            "→ NSQF Level",
            training["nsqf_level"]
        )
        