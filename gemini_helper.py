from google import genai

client = genai.Client(
    api_key="AIzaSyB8gCy-R8mGCame_LDKt3-26TpbWBZX27Y"
)

def analyze_resume(resume_text):

    prompt = f"""
    You are a senior technical recruiter.

    Analyze this resume.

    Return:

    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. Career Suggestions
    5. Interview Readiness Score out of 10

    Resume:

    {resume_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text