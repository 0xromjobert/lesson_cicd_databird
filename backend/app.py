import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

# CORS : autoriser le frontend local ET déployé sur Render
app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:3000",  # développement local
    "https://frontend-app-x026.onrender.com"
])


db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "dbname": os.getenv("POSTGRES_DB", "mydb"),
    "user": os.getenv("POSTGRES_USER", "dev"),
    "password": os.getenv("POSTGRES_PASSWORD", "dev")
}


def get_connection():
    return psycopg2.connect(**db_config)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


init_db()


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


@app.route("/messages", methods=["GET"])
def get_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, content, created_at FROM messages "
        "ORDER BY created_at DESC;"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"id": r[0], "content": r[1], "created_at": r[2].isoformat()}
        for r in rows
    ])


@app.route("/messages", methods=["POST"])
def post_message():
    print("POST /messages triggered")
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (content) VALUES (%s) RETURNING id;",
        (content,)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Message added", "id": new_id}), 201


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
