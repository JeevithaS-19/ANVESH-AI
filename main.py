from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

from integrations.whatsapp.whatsapp_webhook import router as whatsapp_router


app = FastAPI(
    title="ANVESH AI",
    version="1.0.0"
)

# WhatsApp integration
app.include_router(whatsapp_router)


@app.get("/")
def home():
    return {
        "message": "ANVESH AI integration server is running"
    }


# Voice integration
@app.post("/voice")
def voice():
    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/voice/process",
        method="POST",
        language="en-IN",
        speech_timeout="auto"
    )

    gather.say(
        "Welcome to ANVESH AI. Please tell me your name.",
        language="en-IN"
    )

    response.append(gather)

    return Response(
        content=str(response),
        media_type="application/xml"
    )


@app.post("/voice/process")
def voice_process(SpeechResult: str = Form("")):
    response = VoiceResponse()

    response.say(
        f"Hello {SpeechResult}. Welcome to ANVESH AI.",
        language="en-IN"
    )

    return Response(
        content=str(response),
        media_type="application/xml"
    )