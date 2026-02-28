import google.genai as genai
import os

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_response(prompt):
    return client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )