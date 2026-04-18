from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @app.post("/api/v1/echo")
    def echo_message() -> tuple[dict[str, Any], int]:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "JSON object body is required"}), 400

        message = payload.get("message")
        if not isinstance(message, str):
            return jsonify({"error": "'message' must be a string"}), 400

        cleaned = message.strip()
        if not cleaned:
            return jsonify({"error": "'message' cannot be empty"}), 400
        if len(cleaned) > 200:
            return jsonify({"error": "'message' cannot exceed 200 characters"}), 400

        # Reject control characters to reduce log/terminal injection risk.
        if any(ord(ch) < 32 for ch in cleaned):
            return jsonify({"error": "'message' contains invalid characters"}), 400

        return jsonify({"echo": cleaned}), 200

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
