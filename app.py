from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your OpenRouter API Key
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "SaatBot"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are SaatBot, a professional AI assistant. Answer all questions clearly and intelligently."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        ai_reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "response": ai_reply
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)