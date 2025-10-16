from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Load Google API key from environment variable
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

# Configure Google's Generative AI
if google_api_key:
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
    else:
        print(f"✅ Google Gemini API configured with key: {google_api_key[:20]}...")
else:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment variables or .env file!")
    print("Please check your .env file and make sure GOOGLE_API_KEY is set.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"reply": "Please type something!"})

    if not google_api_key:
        return jsonify({"reply": "❌ ERROR: Google API key not configured. Please check your .env file."})

    if not model:
        return jsonify({"reply": "❌ ERROR: No Gemini models available. Please check your Google API access and billing."})

    try:
        # Generate response using Google's Gemini
        response = model.generate_content(user_input)
        reply = response.text.strip()

        if not reply:
            reply = "I couldn't generate a response. Please try again."

        return jsonify({"reply": reply})

    except Exception as e:
        error_msg = str(e)
        print(f"Google API Error: {error_msg}")

        if "API_KEY" in error_msg or "authentication" in error_msg.lower():
            return jsonify({"reply": "❌ ERROR: Invalid Google API key. Please check your API key in the .env file."})
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return jsonify({"reply": "❌ ERROR: Google API quota exceeded. Please check your billing or usage limits."})
        elif "model" in error_msg.lower() or "not found" in error_msg.lower():
            # Fallback: Provide a mock response for testing
            mock_responses = [
                "I'm currently using a demo mode since the Gemini API isn't available. Your message was: " + user_input,
                "This is a test response. To get real AI responses, please get a proper Gemini API key from Google AI Studio.",
                "Demo mode active. Please configure a valid Gemini API key to get intelligent responses."
            ]
            import random
            reply = random.choice(mock_responses)
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": f"❌ Sorry, I encountered an error: {error_msg}"})

if __name__ == "__main__":
    print(f"🤖 BHAVESH GPT with Google Gemini AI")
    print(f"📊 API Key loaded: {google_api_key[:20]}..." if google_api_key else "❌ No API key found!")
    app.run(host="127.0.0.1", port=5000, debug=True)