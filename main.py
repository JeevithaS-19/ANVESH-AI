from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ANVESH AI WhatsApp server is running"}


@app.post("/whatsapp")
def whatsapp(Body: str = Form(...)):
    response = MessagingResponse()
    response.message(f"ANVESH AI received: {Body}")

    return Response(
        content=str(response),
        media_type="application/xml"
    )
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather


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