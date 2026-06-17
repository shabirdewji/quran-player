from flask import Flask, render_template, jsonify
import sqlite3
import os
from urllib.parse import quote
from surahs import surahs

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "quran.db")

BASE_URL = "https://dn710705.ca.archive.org/0/items/MishariRashidWithIbrahimWalk-SaheehIntl-English"


# ---------------- DB ----------------

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def build_url(filename):
    return f"{BASE_URL}/{quote(filename)}"


# ---------------- HOME ----------------

@app.route("/")
def index():
    data = []

    for surah_id, name, filename in surahs:
        data.append({
            "id": surah_id,
            "name": name,
            "url": build_url(filename)   # ✅ SYSTEM A FIX
        })

    return render_template("index.html", surahs=data)


# ---------------- AYAH API ----------------

@app.route("/surah/<int:surah_id>")
def get_surah(surah_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT ayah, text
        FROM quran
        WHERE surah = ?
        ORDER BY ayah ASC
    """, (surah_id,))

    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {"ayah": r[0], "text": r[1]}
        for r in rows
    ])


if __name__ == "__main__":
    app.run(debug=True)