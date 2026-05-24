from google import genai

client = genai.Client(
    api_key="AIzaSyB8gCy-R8mGCame_LDKt3-26TpbWBZX27Y"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me in one sentence why DevOps is important."
)

print(response.text)