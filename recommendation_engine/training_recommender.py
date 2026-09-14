def recommend_training(occupation_result, occupations):
    occupation_name = occupation_result["occupation"]
    missing_skills = occupation_result["missing_skills"]

    for occupation in occupations:
        if occupation["name"] == occupation_name:

            recommendations = []

            for training in occupation.get("training", []):
                # PostgreSQL knowledge base already stores
                # training details including NSQF level.
                if isinstance(training, dict):
                    recommendations.append({
                        "training": training.get("training", ""),
                        "nsqf_level": training.get("nsqf_level", ""),
                        "provider": training.get("provider", ""),
                        "mode": training.get("mode", ""),
                        "duration_weeks": training.get("duration_weeks", 0),
                        "linked_skills": training.get("linked_skills", [])
                    })
                else:
                    # Backward compatibility with old knowledge-base format
                    recommendations.append({
                        "training": training,
                        "nsqf_level": ""
                    })

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