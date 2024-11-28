from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('returns.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS laptop_returns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        san TEXT NOT NULL,
        returned_by TEXT NOT NULL,
        returned_to TEXT NOT NULL,
        notes TEXT
    )''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    san = request.form['san']
    returned_by = request.form['returned_by']
    returned_to = request.form['returned_to']
    notes = request.form.get('notes', '')

    conn = sqlite3.connect('returns.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO laptop_returns (san, returned_by, returned_to, notes) VALUES (?, ?, ?, ?)",
                   (san, returned_by, returned_to, notes))
    conn.commit()
    conn.close()
    return "Form submitted successfully!"

if __name__ == "__main__":
    init_db()  # Call this manually to ensure the database is created
    app.run(host="0.0.0.0", port=8080, debug=True)