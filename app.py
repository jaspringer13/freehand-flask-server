from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/parse_intent", methods=["POST"])
def parse_intent():
    try:
        # Safely parse JSON payload
        data = request.get_json(force=True)
        print("Incoming data:", data)

        # Handle if speech field is missing
        user_input = data.get("speech", "I didn't catch that.")

        # Call OpenAI ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for a local business. Be concise and helpful."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        # Extract reply and return to Twilio
        reply = response['choices'][0]['message']['content']
        return jsonify({"result": reply})
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

# Optional: a basic health check route
@app.route("/")
def index():
    return "FreeHand Flask server is running."
