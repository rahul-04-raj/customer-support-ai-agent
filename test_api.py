"""Quick test to verify the Gemini API key and find available models."""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"Key starts with: {api_key[:10]}..." if api_key else "")

from google import genai

client = genai.Client(api_key=api_key)

# List available models
print("\n--- Available Gemini Models ---")
for model in client.models.list():
    if "gemini" in model.name.lower():
        print(f"  {model.name}")

# Try a simple call
print("\n--- Testing generation ---")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello in one sentence.",
    )
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"FAILED with gemini-2.0-flash: {e}")
    # Try fallback
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="Say hello in one sentence.",
        )
        print(f"SUCCESS with gemini-2.0-flash-lite: {response.text}")
    except Exception as e2:
        print(f"FAILED with gemini-2.0-flash-lite: {e2}")
