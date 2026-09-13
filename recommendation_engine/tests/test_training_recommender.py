from recommendation_engine.recommendation_engine import (
    OCCUPATIONS
)

from recommendation_engine.training_recommender import (
    recommend_training
)


def test_training_recommendation():

    occupation = next(
        occupation
        for occupation in OCCUPATIONS
        if occupation["name"] == "Data Analyst"
    )

    result = {
        "occupation": occupation["name"],
        "missing_skills": [
            "Data Analysis",
            "Data Visualization",
            "Statistics"
        ]
    }

    recommendation = recommend_training(
        result,
        OCCUPATIONS
    )

    assert isinstance(recommendation, dict)
    assert recommendation["occupation"] == "Data Analyst"
    assert "missing_skills" in recommendation
    assert "recommendations" in recommendation

    assert isinstance(
        recommendation["recommendations"],
        list
    )

    for training in recommendation["recommendations"]:

        assert isinstance(training, dict)

        assert "training" in training
        assert "nsqf_level" in training
        assert "provider" in training
        assert "mode" in training
        assert "duration_weeks" in training
        assert "priority" in training
        assert "relevant_missing_skills" in training