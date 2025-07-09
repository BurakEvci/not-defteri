from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    database=os.environ.get("DB_NAME", "notes_db"),
    user=os.environ.get("DB_USER", "burak"),
    password=os.environ.get("DB_PASS", "1234")
)
cur = conn.cursor()

# TABLOYU OLUŞTUR
cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL
    );
""")
conn.commit()

# Basit HTML arayüz
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Not Defteri</title></head>
<body>
    <h1>Notlar</h1>
    <ul>
        {% for note in notes %}
            <li>{{ note[0] }} - {{ note[1] }}</li>
        {% endfor %}
    </ul>
    <form action="/notes" method="post">
        <input type="text" name="content" placeholder="Yeni not..." required>
        <button type="submit">Ekle</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    cur.execute("SELECT id, content FROM notes ORDER BY id ASC;")
    notes = cur.fetchall()
    return render_template_string(HTML_TEMPLATE, notes=notes)

@app.route("/notes", methods=["GET"])
def get_notes():
    cur.execute("SELECT id, content FROM notes ORDER BY id ASC;")
    return jsonify([{"id": row[0], "content": row[1]} for row in cur.fetchall()])

@app.route("/notes", methods=["POST"])
def add_note():
    content = request.form.get("content") or request.json.get("content")
    cur.execute("INSERT INTO notes (content) VALUES (%s) RETURNING id;", (content,))
    note_id = cur.fetchone()[0]
    conn.commit()
    return jsonify({"id": note_id, "content": content}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
