from recommendation_engine.recommendation_engine import (
    generate_recommendations
)


def test_generate_recommendations():

    results = generate_recommendations(
        user_skills=["Python", "SQL", "Excel"],
        education="B.Tech",
        experience="1 year",
        interests=["Data Analysis", "Technology"],
        career_goal="analytics",
        location="Bengaluru"
    )

    assert isinstance(results, list)
    assert len(results) > 0

    first_result = results[0]

    assert "occupation" in first_result
    assert "compatibility_score" in first_result
    assert "match_percentage" in first_result
    assert "matched_skills" in first_result
    assert "missing_skills" in first_result
    assert "training" in first_result
    assert "skill_pathway" in first_result
    assert "recommendation_summary" in first_result

    assert isinstance(first_result["compatibility_score"], (int, float))
    assert isinstance(first_result["match_percentage"], (int, float))

    print("\n===== ANVESH AI RECOMMENDATIONS =====")

    for index, result in enumerate(results, start=1):

        print(f"\n{index}. {result['occupation']}")
        print(
            f"Compatibility Score: "
            f"{result['compatibility_score']}"
        )
        print(
            f"Skill Match: "
            f"{result['match_percentage']}%"
        )
        print(
            f"Matched Skills: "
            f"{result['matched_skills']}"
        )
        print(
            f"Missing Skills: "
            f"{result['missing_skills']}"
        )