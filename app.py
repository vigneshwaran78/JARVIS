from __future__ import annotations

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from jarvis.agent import JarvisAgent

app = Flask(__name__)
CORS(app)
agent = JarvisAgent()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"response": "Please enter a message."}), 400
    try:
        reply = agent.run(message)
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
