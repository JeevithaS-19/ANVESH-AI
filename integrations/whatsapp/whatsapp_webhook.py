import os
from typing import Any

import httpx
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from integrations.whatsapp.whatsapp_service import format_recommendation_response


router = APIRouter()

sessions: dict[str, dict[str, Any]] = {}

RECOMMENDATION_API_URL = os.getenv(
    "RECOMMENDATION_API_URL",
    "http://127.0.0.1:8001/recommendations/",
)


def validate_twilio_request(request: Request, form_data) -> None:
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not auth_token:
        raise HTTPException(
            status_code=500,
            detail="Twilio Auth Token is not configured"
        )

    signature = request.headers.get("X-Twilio-Signature", "")

    validator = RequestValidator(auth_token)

    if not validator.validate(
        str(request.url),
        dict(form_data),
        signature
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid Twilio signature"
        )


def twiml_response(message: str) -> Response:
    response = MessagingResponse()
    response.message(message)

    return Response(
        content=str(response),
        media_type="application/xml"
    )


def normalize_list(value: str) -> list[str]:
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


async def get_recommendations(profile: dict[str, Any]) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            RECOMMENDATION_API_URL,
            json=profile
        )

        response.raise_for_status()

        return response.json()


@router.post("/whatsapp")
async def whatsapp(
    request: Request,
    Body: str = Form(...),
    From: str = Form("")
):
    form_data = await request.form()

    # Security: verify request came from Twilio
    validate_twilio_request(request, form_data)

    sender = From or "unknown"
    message = Body.strip()

    if not message:
        return twiml_response(
            "Please send a message to continue."
        )

    lower_message = message.lower()

    if lower_message in {
        "hi",
        "hello",
        "hey",
        "start",
        "menu",
        "restart"
    }:
        sessions[sender] = {
            "step": "education",
            "profile": {
                "skills": [],
                "education": "",
                "experience": "",
                "interests": [],
                "career_goal": "",
                "location": "",
            },
        }

        return twiml_response(
            "👋 *Welcome to ANVESH AI!*\n\n"
            "I can help you find suitable career, training "
            "and livelihood opportunities.\n\n"
            "Let's create your profile.\n\n"
            "🎓 *Step 1/6*\n"
            "What is your highest educational qualification?"
        )

    if sender not in sessions:
        sessions[sender] = {
            "step": "education",
            "profile": {
                "skills": [],
                "education": "",
                "experience": "",
                "interests": [],
                "career_goal": "",
                "location": "",
            },
        }

        return twiml_response(
            "👋 Welcome to ANVESH AI!\n\n"
            "Let's create your profile.\n\n"
            "🎓 What is your highest educational qualification?"
        )

    session = sessions[sender]
    step = session["step"]
    profile = session["profile"]

    if step == "education":
        profile["education"] = message
        session["step"] = "skills"

        return twiml_response(
            "🛠️ *Step 2/6*\n"
            "What skills do you have?\n\n"
            "Example:\n"
            "Python, Excel, tailoring, farming"
        )

    if step == "skills":
        profile["skills"] = normalize_list(message)
        session["step"] = "experience"

        return twiml_response(
            "💼 *Step 3/6*\n"
            "Tell me about your work experience.\n\n"
            "If you have no experience, type *Fresher*."
        )

    if step == "experience":
        profile["experience"] = message
        session["step"] = "interests"

        return twiml_response(
            "⭐ *Step 4/6*\n"
            "What are your interests?\n\n"
            "Example:\n"
            "Technology, business, farming"
        )

    if step == "interests":
        profile["interests"] = normalize_list(message)
        session["step"] = "career_goal"

        return twiml_response(
            "🎯 *Step 5/6*\n"
            "What is your career goal?\n\n"
            "Example:\n"
            "Get a software job"
        )

    if step == "career_goal":
        profile["career_goal"] = message
        session["step"] = "location"

        return twiml_response(
            "📍 *Step 6/6*\n"
            "Which city or location are you looking for "
            "opportunities in?"
        )

    if step == "location":
        profile["location"] = message

        try:
            result = await get_recommendations(profile)

            response_text = format_recommendation_response(
                result
            )

            sessions.pop(sender, None)

            return twiml_response(response_text)

        except httpx.HTTPError as error:
            print(f"Recommendation API error: {error}")

            return twiml_response(
                "⚠️ ANVESH AI could not connect to the "
                "recommendation service right now.\n\n"
                "Please try again later."
            )

        except Exception as error:
            print(
                f"Unexpected WhatsApp integration error: {error}"
            )

            return twiml_response(
                "⚠️ Something went wrong while generating "
                "your recommendation.\n\n"
                "Please try again."
            )

    return twiml_response(
        "Please type *HI* to start ANVESH AI."
    )