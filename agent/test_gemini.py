import os
import time
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file.")

# Create Gemini client
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"      # Replace with your preferred model

print("=" * 50)
print("      Gemini API Test")
print("=" * 50)
print(f"Model      : {MODEL_NAME}")
print("Status     : Connecting...")
print()

try:
    start = time.time()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Introduce yourself in one sentence."
    )

    end = time.time()

    print("✅ Connection Successful!\n")
    print("Response:")
    print("-" * 50)
    print(response.text)
    print("-" * 50)
    print(f"Response Time : {end - start:.2f} seconds")

except Exception as e:
    print("❌ Request Failed")
    print(f"Error Type : {type(e).__name__}")
    print(f"Message    : {e}")

print("=" * 50)