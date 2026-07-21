#import os
#from dotenv import load_dotenv
from google import genai
from config import GOOGLE_API_KEY, GEMINI_MODEL

#load_dotenv()

client = genai.Client(api_key=GOOGLE_API_KEY)

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
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text