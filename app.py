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


@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "status": "online",
        "model": agent.configured_model,
        "memory_count": len(agent.memory.history()),
        "voice_enabled": agent.voice_enabled,
    })


@app.route("/api/memory", methods=["GET"])
def get_memory():
    return jsonify({
        "history": agent.memory.history(),
        "count": len(agent.memory.history()),
    })


@app.route("/api/memory/clear", methods=["POST"])
def clear_memory():
    try:
        agent.clear_memory()
        return jsonify({"success": True, "message": "Memory cleared."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
