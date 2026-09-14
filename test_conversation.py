from voice_ai.pipeline.voice_pipeline import VoicePipeline


# ============================================================
# ANVESH AI - COMPLETE CONVERSATION FLOW TEST
# ============================================================

pipeline = VoicePipeline()


conversation = [

    # --------------------------------------------------------
    # 1. JOB REQUIREMENT
    # --------------------------------------------------------
    "I am looking for a software development job",

    # --------------------------------------------------------
    # 2. NAME
    # --------------------------------------------------------
    "My name is Ravi Kumar",

    # --------------------------------------------------------
    # 3. MULTIPLE EDUCATION QUALIFICATIONS
    # --------------------------------------------------------
    "I completed B.Tech and MBA",

    # ANVESH asks:
    # Do you have any other educational qualifications?

    "Yes",

    # ANVESH asks:
    # What is your highest level of education?

    "I also completed a diploma",

    # ANVESH asks again:
    # Do you have any other educational qualifications?

    "No",

    # --------------------------------------------------------
    # 4. MULTIPLE SKILLS
    # --------------------------------------------------------
    "I have skills in Python Java React and GitHub",

    # ANVESH asks:
    # Do you have any other skills?

    "Yes",

    # ANVESH asks:
    # What skills do you have?

    "I also know Docker and PostgreSQL",

    # ANVESH asks again:
    # Do you have any other skills?

    "No",

    # --------------------------------------------------------
    # 5. EXPERIENCE
    # --------------------------------------------------------
    "I have 2 years of experience",

    # --------------------------------------------------------
    # 6. LOCATION
    # --------------------------------------------------------
    "I am looking for jobs in Bangalore"
]


# ============================================================
# RUN CONVERSATION
# ============================================================

for turn_number, user_input in enumerate(conversation, start=1):

    print("\n")
    print("=" * 75)
    print(f"TURN {turn_number}")
    print("=" * 75)

    print("\nUSER:")
    print(user_input)

    try:

        result = pipeline.process_text(user_input)

        print("\nLANGUAGE:")
        print(result["language"]["language_code"])

        print("\nTRANSCRIPTION:")
        print(result["transcription"])

        print("\nNEXT QUESTION:")
        print(result["next_question"])

        print("\nPROFILE:")
        print(result["profile"])

        print("\nPROFILE COMPLETE:")
        print(result["profile_complete"])

        print("\nTTS:")
        print(result["tts"])

    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__, "-", e)

        break


# ============================================================
# FINAL PROFILE
# ============================================================

print("\n")
print("=" * 75)
print("FINAL ANVESH AI PROFILE")
print("=" * 75)

final_profile = pipeline.conversation.get_profile()

for key, value in final_profile.items():

    print(f"{key}: {value}")


print("\n")
print("=" * 75)

if pipeline.conversation.is_profile_complete():

    print("SUCCESS: PROFILE COMPLETE")

else:

    print("PROFILE INCOMPLETE")

print("=" * 75)