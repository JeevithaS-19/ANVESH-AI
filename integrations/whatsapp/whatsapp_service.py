from typing import Any


def format_recommendation_response(data: dict[str, Any]) -> str:
    """
    Convert ANVESH AI recommendation API output
    into a WhatsApp-friendly message.
    """

    recommendations = data.get("recommendations", [])

    if not recommendations:
        return (
            "Sorry, I could not find a suitable recommendation "
            "from the available data."
        )

    recommendation = recommendations[0]

    occupation = recommendation.get("occupation", "Not available")
    score = recommendation.get("compatibility_score", 0)

    matched_skills = recommendation.get("matched_skills", [])
    missing_skills = recommendation.get("missing_skills", [])
    explanation = recommendation.get("explanation", "")

    lines = [
        "🤖 *ANVESH AI Recommendation*",
        "",
        f"🎯 *Recommended Occupation:* {occupation}",
        f"📊 *Compatibility Score:* {score}%",
        "",
    ]

    if matched_skills:
        lines.append("✅ *Matching Skills:*")
        lines.append(", ".join(matched_skills))
        lines.append("")

    if missing_skills:
        lines.append("📚 *Skills to Develop:*")
        lines.append(", ".join(missing_skills))
        lines.append("")

    training = recommendation.get("training", {})

    training_items = training.get("recommendations", [])

    if training_items:
        lines.append("🎓 *NSQF Training Recommendations:*")

        for item in training_items[:3]:
            if isinstance(item, dict):
                title = item.get("title", item.get("name", "Training"))
                lines.append(f"• {title}")
            else:
                lines.append(f"• {item}")

        lines.append("")

    opportunities = recommendation.get("opportunities", [])

    if opportunities:
        lines.append("💼 *Opportunities:*")

        for opportunity in opportunities[:3]:
            if isinstance(opportunity, dict):
                title = opportunity.get("title", "Opportunity")
                location = opportunity.get("location", "")

                if location:
                    lines.append(f"• {title} — {location}")
                else:
                    lines.append(f"• {title}")

        lines.append("")

    if explanation:
        lines.append("💡 *Why this is recommended:*")
        lines.append(explanation)

    lines.append("")
    lines.append("Reply *MENU* to start again.")

    return "\n".join(lines)