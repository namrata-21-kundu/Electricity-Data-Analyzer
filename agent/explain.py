import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = "gemini-3.6-flash"

def explain(question, analysis_result):
    prompt = f"""
You are an electricity consumption analyst.

The user asked:

{question}

Analysis Result:

{analysis_result}

Explain the results in simple English.

If appropriate, suggest practical ways to reduce electricity consumption.

Do not invent any values.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text