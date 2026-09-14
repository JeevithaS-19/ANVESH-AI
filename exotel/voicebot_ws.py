import asyncio
import base64
import json
import os
import tempfile
import time
import wave
from array import array

import imageio_ffmpeg
import websockets

from voice_ai.pipeline.voice_pipeline import VoicePipeline


# ============================================================
# ANVESH AI - EXOTEL VOICEBOT SERVER
# ============================================================


# ============================================================
# AUDIO CONFIGURATION
# ============================================================

SAMPLE_RATE = 8000
CHANNELS = 1
SAMPLE_WIDTH = 2


# ============================================================
# VOICE ACTIVITY DETECTION
# ============================================================

# RMS threshold for detecting speech
SILENCE_THRESHOLD = 850

# Do not process tiny noises as speech
MIN_SPEECH_MS = 800

# Wait for a natural pause before processing speech
SILENCE_MS = 2000

# Ignore residual phone/echo audio after ANVESH finishes speaking
POST_TTS_IGNORE_MS = 700


# ============================================================
# PCM -> WAV
# ============================================================

def pcm_to_wav(pcm_data, output_file):

    with wave.open(output_file, "wb") as wav:

        wav.setnchannels(CHANNELS)
        wav.setsampwidth(SAMPLE_WIDTH)
        wav.setframerate(SAMPLE_RATE)

        wav.writeframes(pcm_data)


# ============================================================
# RMS CALCULATION
# ============================================================

def calculate_rms(pcm_data):

    if not pcm_data:
        return 0

    samples = array("h")

    try:
        samples.frombytes(pcm_data)

    except Exception:
        return 0

    if not samples:
        return 0

    total = sum(
        sample * sample
        for sample in samples
    )

    return (
        total / len(samples)
    ) ** 0.5


# ============================================================
# MP3 -> PCM
# ============================================================

async def mp3_to_pcm(mp3_file):

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    process = await asyncio.create_subprocess_exec(

        ffmpeg,

        "-y",

        "-i",
        mp3_file,

        "-f",
        "s16le",

        "-acodec",
        "pcm_s16le",

        "-ac",
        "1",

        "-ar",
        str(SAMPLE_RATE),

        "pipe:1",

        stdout=asyncio.subprocess.PIPE,

        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:

        raise RuntimeError(
            "FFmpeg conversion failed:\n"
            + stderr.decode(errors="ignore")
        )

    return stdout


# ============================================================
# SPLIT PCM
# ============================================================

def split_pcm(pcm_data, chunk_size=3200):

    for index in range(
        0,
        len(pcm_data),
        chunk_size
    ):

        yield pcm_data[
            index:
            index + chunk_size
        ]


# ============================================================
# SEND TTS AUDIO TO EXOTEL
# ============================================================

async def send_audio(
    websocket,
    stream_sid,
    pcm_data
):

    for chunk in split_pcm(
        pcm_data
    ):

        if len(chunk) < 320:
            continue

        message = {

            "event": "media",

            "stream_sid": stream_sid,

            "media": {

                "payload":
                    base64.b64encode(
                        chunk
                    ).decode("ascii")
            }
        }

        await websocket.send(
            json.dumps(message)
        )

        # Approximate real-time playback
        await asyncio.sleep(0.18)


# ============================================================
# PROCESS CALLER AUDIO
# ============================================================

async def process_caller_audio(
    websocket,
    stream_sid,
    pcm_buffer,
    pipeline,
    state
):

    if not pcm_buffer:
        state["bot_speaking"] = False
        state["processing"] = False
        return

    wav_file = None

    # ========================================================
    # LOCK PROCESSING
    # ========================================================

    # These are also set before create_task()
    # in the WebSocket loop.
    #
    # Keeping them here provides an additional safety layer.

    state["processing"] = True
    state["bot_speaking"] = True

    try:

        # ====================================================
        # CREATE TEMPORARY WAV
        # ====================================================

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            wav_file = temp.name

        pcm_to_wav(
            bytes(pcm_buffer),
            wav_file
        )

        print()
        print(
            "[ANVESH] Processing caller audio..."
        )

        # ====================================================
        # SAME PIPELINE FOR ENTIRE CALL
        # ====================================================

        result = await asyncio.to_thread(
            pipeline.process_audio,
            wav_file
        )

        # ====================================================
        # TRANSCRIPTION
        # ====================================================

        transcription = (
            result.get(
                "transcription",
                ""
            )
        )

        print(
            "[ANVESH] Transcription:",
            transcription
        )

        # ====================================================
        # LANGUAGE
        # ====================================================

        print(
            "[ANVESH] Language:",
            result.get("language")
        )

        # ====================================================
        # INTENT
        # ====================================================

        print(
            "[ANVESH] Intent:",
            result.get(
                "profile",
                {}
            ).get("intent")
        )

        # ====================================================
        # NEXT QUESTION
        # ====================================================

        print(
            "[ANVESH] Next question:",
            result.get("next_question")
        )

        # ====================================================
        # PROFILE
        # ====================================================

        print(
            "[ANVESH] Profile:",
            result.get("profile")
        )

        # ====================================================
        # PROFILE COMPLETE
        # ====================================================

        print(
            "[ANVESH] Complete:",
            result.get("profile_complete")
        )

        # ====================================================
        # EMPTY TRANSCRIPTION
        # ====================================================

        if not transcription.strip():

            print(
                "[ANVESH] Empty transcription."
                " Ignoring."
            )

            return

        # ====================================================
        # DUPLICATE TRANSCRIPTION PROTECTION
        # ====================================================

        normalized = " ".join(
            transcription
            .lower()
            .split()
        )

        previous = state.get(
            "last_transcription"
        )

        previous_time = state.get(
            "last_transcription_time",
            0
        )

        now = time.monotonic()

        if (
            normalized == previous
            and
            now - previous_time < 3
        ):

            print(
                "[ANVESH] Duplicate "
                "transcription ignored."
            )

            return

        state["last_transcription"] = normalized
        state["last_transcription_time"] = now

        # ====================================================
        # TTS
        # ====================================================

        tts_result = result.get("tts")

        if not tts_result:

            print(
                "[ANVESH] No TTS result."
            )

            return

        if not tts_result.get("success"):

            print(
                "[ANVESH] TTS failed:",
                tts_result.get("error")
            )

            return

        # ====================================================
        # PROFILE COMPLETE
        # ====================================================

        if result.get("profile_complete"):

            print(
                "[ANVESH] Profile complete."
            )

            return

        # ====================================================
        # TTS AUDIO FILE
        # ====================================================

        mp3_file = tts_result.get(
            "audio_file"
        )

        if not mp3_file:

            print(
                "[ANVESH] TTS audio file missing."
            )

            return

        # ====================================================
        # MP3 -> PCM
        # ====================================================

        print(
            "[ANVESH] Converting TTS audio..."
        )

        pcm_response = await mp3_to_pcm(
            mp3_file
        )

        print(
            "[ANVESH] PCM bytes:",
            len(pcm_response)
        )

        # ====================================================
        # SEND AUDIO TO CALLER
        # ====================================================

        print(
            "[ANVESH] Sending audio to caller..."
        )

        await send_audio(
            websocket,
            stream_sid,
            pcm_response
        )

        print(
            "[ANVESH] Response sent."
        )

        # ====================================================
        # IGNORE RESIDUAL AUDIO / ECHO
        # ====================================================

        state["ignore_audio_until"] = (
            time.monotonic()
            +
            POST_TTS_IGNORE_MS / 1000
        )

    except Exception as error:

        print(
            "[ANVESH ERROR]",
            repr(error)
        )

    finally:

        # ====================================================
        # REMOVE TEMPORARY WAV
        # ====================================================

        if (
            wav_file
            and
            os.path.exists(wav_file)
        ):

            try:

                os.remove(wav_file)

            except Exception:
                pass

        # ====================================================
        # UNLOCK
        # ====================================================

        state["bot_speaking"] = False
        state["processing"] = False

        # ====================================================
        # CLEAR AUDIO THAT ARRIVED WHILE BOT WAS SPEAKING
        # ====================================================

        state["pcm_buffer"] = bytearray()

        state["speech_started"] = False

        state["speech_duration_ms"] = 0

        state["silence_duration_ms"] = 0


# ============================================================
# HANDLE EXOTEL CONNECTION
# ============================================================

async def handle_connection(websocket):

    stream_sid = None

    # ========================================================
    # ONE PIPELINE PER CALL
    # ========================================================

    pipeline = VoicePipeline()

    # ========================================================
    # CALL STATE
    # ========================================================

    state = {

        "pcm_buffer":
            bytearray(),

        "speech_started":
            False,

        "speech_duration_ms":
            0,

        "silence_duration_ms":
            0,

        "processing":
            False,

        "bot_speaking":
            False,

        "ignore_audio_until":
            0,

        "last_transcription":
            None,

        "last_transcription_time":
            0,
    }

    print()
    print(
        "===================================="
    )

    print(
        "[EXOTEL] WebSocket connected."
    )

    print(
        "===================================="
    )

    try:

        async for message in websocket:

            # =================================================
            # IGNORE BINARY
            # =================================================

            if isinstance(
                message,
                bytes
            ):

                continue

            # =================================================
            # PARSE JSON
            # =================================================

            try:

                event = json.loads(
                    message
                )

            except Exception:

                print(
                    "[EXOTEL] Invalid JSON."
                )

                continue

            event_type = event.get(
                "event"
            )

            # =================================================
            # CONNECTED
            # =================================================

            if event_type == "connected":

                print(
                    "[EXOTEL] Connected event received."
                )

            # =================================================
            # START
            # =================================================

            elif event_type == "start":

                start_data = event.get(
                    "start",
                    {}
                )

                stream_sid = start_data.get(
                    "stream_sid"
                )

                media_format = start_data.get(
                    "media_format",
                    {}
                )

                print(
                    "[EXOTEL] Stream started:"
                )

                print(
                    "  Stream SID:",
                    stream_sid
                )

                print(
                    "  Audio format:",
                    media_format
                )

                # =============================================
                # RESET CALL
                # =============================================

                pipeline.reset()

                state["pcm_buffer"] = bytearray()

                state["speech_started"] = False

                state["speech_duration_ms"] = 0

                state["silence_duration_ms"] = 0

                state["processing"] = False

                state["bot_speaking"] = False

                state["ignore_audio_until"] = 0

                state["last_transcription"] = None

                state["last_transcription_time"] = 0

            # =================================================
            # MEDIA
            # =================================================

            elif event_type == "media":

                media = event.get(
                    "media",
                    {}
                )

                payload = media.get(
                    "payload"
                )

                if not payload:
                    continue

                # =================================================
                # DO NOT PROCESS AUDIO WHILE BOT IS SPEAKING
                # =================================================

                if (
                    state["bot_speaking"]
                    or
                    state["processing"]
                ):

                    continue

                # =================================================
                # IGNORE RESIDUAL AUDIO
                # =================================================

                if (
                    time.monotonic()
                    <
                    state[
                        "ignore_audio_until"
                    ]
                ):

                    continue

                # =================================================
                # DECODE AUDIO
                # =================================================

                try:

                    audio_chunk = (
                        base64.b64decode(
                            payload
                        )
                    )

                except Exception:

                    continue

                # =================================================
                # ADD TO BUFFER
                # =================================================

                state[
                    "pcm_buffer"
                ].extend(
                    audio_chunk
                )

                # =================================================
                # RMS
                # =================================================

                rms = calculate_rms(
                    audio_chunk
                )

                # Exotel packet ≈ 100 ms
                chunk_ms = 100

                # =================================================
                # SPEECH DETECTED
                # =================================================

                if rms > SILENCE_THRESHOLD:

                    state[
                        "speech_started"
                    ] = True

                    state[
                        "speech_duration_ms"
                    ] += chunk_ms

                    state[
                        "silence_duration_ms"
                    ] = 0

                # =================================================
                # SILENCE DETECTED
                # =================================================

                elif state[
                    "speech_started"
                ]:

                    state[
                        "silence_duration_ms"
                    ] += chunk_ms

                # =================================================
                # SPEECH COMPLETE
                # =================================================

                if (
                    state[
                        "speech_started"
                    ]

                    and

                    state[
                        "speech_duration_ms"
                    ]
                    >= MIN_SPEECH_MS

                    and

                    state[
                        "silence_duration_ms"
                    ]
                    >= SILENCE_MS

                    and

                    not state[
                        "processing"
                    ]
                ):

                    print(
                        "[EXOTEL] Speech segment complete."
                    )

                    # =========================================
                    # COPY BUFFER
                    # =========================================

                    audio_to_process = (
                        state[
                            "pcm_buffer"
                        ]
                    )

                    # =========================================
                    # IMPORTANT:
                    #
                    # LOCK IMMEDIATELY BEFORE create_task()
                    #
                    # This prevents another speech segment
                    # from creating another processing task.
                    # =========================================

                    state["processing"] = True
                    state["bot_speaking"] = True

                    # =========================================
                    # RESET INPUT STATE BEFORE PROCESSING
                    # =========================================

                    state[
                        "pcm_buffer"
                    ] = bytearray()

                    state[
                        "speech_started"
                    ] = False

                    state[
                        "speech_duration_ms"
                    ] = 0

                    state[
                        "silence_duration_ms"
                    ] = 0

                    # =========================================
                    # PROCESS EXACTLY ONE SEGMENT
                    # =========================================

                    asyncio.create_task(
                        process_caller_audio(
                            websocket,
                            stream_sid,
                            audio_to_process,
                            pipeline,
                            state
                        )
                    )

            # =================================================
            # DTMF
            # =================================================

            elif event_type == "dtmf":

                digit = (
                    event.get(
                        "dtmf",
                        {}
                    ).get(
                        "digit"
                    )
                )

                print(
                    "[EXOTEL] DTMF:",
                    digit
                )

            # =================================================
            # STOP
            # =================================================

            elif event_type == "stop":

                print(
                    "[EXOTEL] Call/stream stopped."
                )

                break

            # =================================================
            # OTHER EVENTS
            # =================================================

            else:

                print(
                    "[EXOTEL] Event:",
                    event_type
                )

    except websockets.exceptions.ConnectionClosed:

        print(
            "[EXOTEL] WebSocket connection closed."
        )

    except Exception as error:

        print(
            "[EXOTEL ERROR]",
            repr(error)
        )

    finally:

        print(
            "[EXOTEL] Connection handler finished."
        )


# ============================================================
# MAIN
# ============================================================

async def main():

    print()
    print(
        "========================================"
    )

    print(
        "       ANVESH AI EXOTEL SERVER"
    )

    print(
        "========================================"
    )

    print(
        "WebSocket endpoint:"
    )

    print(
        "ws://127.0.0.1:8000/exotel"
    )

    print()

    print(
        "Waiting for Exotel connection..."
    )

    print()

    async with websockets.serve(
        handle_connection,
        "0.0.0.0",
        8000
    ):

        await asyncio.Future()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print()

        print(
            "[ANVESH] Server stopped."
        )