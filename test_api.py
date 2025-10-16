#!/usr/bin/env python3
"""
Simple test script to verify Google Gemini API key is working
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_google_api():
    print("🔍 Checking Google API key...")

    # Load Google API key from environment
    google_api_key = os.getenv('GOOGLE_API_KEY')

    # If not found in environment, try reading directly from .env file
    if not google_api_key:
        try:
            env_file = os.path.join(os.getcwd(), '.env')
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('GOOGLE_API_KEY='):
                            google_api_key = line.split('=', 1)[1].strip()
                            break
        except Exception as e:
            print(f"Error reading .env file: {e}")

    if not google_api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in environment variables or .env file!")
        print("Please check your .env file and make sure GOOGLE_API_KEY is set.")
        return False

    print(f"✅ Google API Key found: {google_api_key[:20]}...")

    try:
        # Configure Google's Generative AI
        genai.configure(api_key=google_api_key)

        # Try different model names in order of preference
        model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']
        model = None

        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✅ Successfully loaded model: {model_name}")
                break
            except Exception as e:
                print(f"⚠️  Model {model_name} not available: {str(e)}")
                continue

        if not model:
            print("❌ ERROR: No available Gemini models found!")
            print("Available models may require different API access or billing.")
            return False

        # Simple test request
        response = model.generate_content("Hello, just testing the Google Gemini API connection. Reply with 'Google Gemini API test successful'")

        reply = response.text.strip()
        print(f"✅ Google Gemini API Test Successful! Response: {reply}")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERROR: {error_msg}")
        if "API_KEY" in error_msg or "authentication" in error_msg.lower():
            print("❌ ERROR: Invalid Google API key. Please check your API key.")
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            print("❌ ERROR: Google API quota exceeded. Please check your billing/usage.")
        else:
            print(f"❌ ERROR: {error_msg}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Google Gemini API Connection...")
    test_google_api()
