from flask import Flask, request, jsonify, render_template_string, render_template, redirect
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



@app.route("/")

def index():
    cur.execute("SELECT id, content FROM notes ORDER BY id ASC;")
    notes = cur.fetchall()
    return render_template("index.html", notes=notes)

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

@app.route("/add", methods=["POST"])
def add_note_via_form():
    content = request.form.get("content")
    if content:
        cur.execute("INSERT INTO notes (content) VALUES (%s);", (content,))
        conn.commit()
    return redirect("/")

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    cur.execute("DELETE FROM notes WHERE id = %s;", (note_id,))
    conn.commit()
    return redirect("/")

@app.route("/jenkins-test")
def jenkins_test():
    return "Merhaba Jenkins'e Hoşgeldin!"

@app.route("/jenkins-test5")
def jenkins_test():
    return "Merhaba Jenkins'e Hoşgeldin Dostum!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
