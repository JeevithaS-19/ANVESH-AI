from voice_ai.pipeline.voice_pipeline import VoicePipeline


pipeline = VoicePipeline()


conversation = [

    # ============================================================
    # ENGLISH
    # ============================================================

    "I am looking for a software development job",

    "My name is Ravi",

    # ============================================================
    # SWITCH TO KANNADA
    # ============================================================

    "Speak in Kannada",

    # ============================================================
    # KANNADA - EDUCATION
    # ============================================================

    "ನಾನು B.Tech ಪೂರ್ಣಗೊಳಿಸಿದ್ದೇನೆ",

    # Confirm no more education
    "No",

    # ============================================================
    # KANNADA - SKILLS
    # ============================================================

    "ನನಗೆ Python ಮತ್ತು Java ಗೊತ್ತು",

    # Confirm no more skills
    "No",

    # ============================================================
    # EXPERIENCE
    # ============================================================

    "I am a fresher",

    # ============================================================
    # LOCATION
    # ============================================================

    "ಬೆಂಗಳೂರು"
]


for turn_number, user_input in enumerate(
    conversation,
    start=1
):

    print("\n" + "=" * 70)
    print(f"TURN {turn_number}")
    print("=" * 70)

    print("\nUSER:")
    print(user_input)

    result = pipeline.process_text(
        user_input
    )

    print("\nLANGUAGE:")
    print(
        result["language"]["language_code"]
    )

    print("\nNEXT QUESTION:")
    print(
        result["next_question"]
    )

    print("\nPROFILE:")
    print(
        result["profile"]
    )

    print("\nPROFILE COMPLETE:")
    print(
        result["profile_complete"]
    )

    print("\nTTS:")
    print(
        result["tts"]
    )


print("\n")
print("=" * 70)
print("FINAL PROFILE")
print("=" * 70)

final_profile = pipeline.conversation.get_profile()

print(final_profile)

print(
    "\nCOMPLETE:",
    pipeline.conversation.is_profile_complete()
)