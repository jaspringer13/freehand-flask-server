from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/parse_intent", methods=["POST"])
def parse_intent():
    data = request.get_json()
    user_input = data.get("SpeechResult", "I didn't catch that.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for a local business. Be concise and helpful."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"result": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
