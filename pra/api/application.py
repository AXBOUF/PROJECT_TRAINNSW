from flask import Flask, jsonify
import psycopg2
from psycopg2 import pool
import os

app = Flask(__name__)

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5432),
    user=os.getenv('POSTGRES_USER', 'mun'),
    password=os.getenv('POSTGRES_PASSWORD', 'admin123'),
    dbname=os.getenv('POSTGRES_DB', 'volleyball_db')
)

def execute(query, params=None, fetch=False, many=False):
    conn = connection_pool.getconn()
    try:
        cursor = conn.cursor()
        if many:
            cursor.executemany(query, params or [])
            conn.commit()
        else:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = None
        cursor.close()
        return result if not many else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection_pool.putconn(conn)

def create_tables():
    execute("""
        CREATE TABLE IF NOT EXISTS volleyball (
            id SERIAL PRIMARY KEY,
            name VARCHAR(80) UNIQUE NOT NULL,
            description VARCHAR(200) NOT NULL
        )
    """)

@app.route('/seed')
def seed():
    players = [
        ("Hinata Shoyo", "Wing Spiker #10"),
        ("Kageyama Tobio", "Setter #9"),
        ("Tsukishima Kei", "Middle Blocker #11"),
        ("Yamaguchi Tadashi", "Middle Blocker #12"),
    ]
    execute(
        "INSERT INTO volleyball (name, description) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
        params=players,
        many=True  # ✅ fixed
    )
    return jsonify({"message": "Seeded!"})

@app.route('/')
def index():
    return "Hinata Shoyo is the best waifu in the world!"

@app.route('/players')
def get_players():
    return jsonify({"players": ["Hinata Shoyo", "Kageyama Tobio", "Tsukishima Kei", "Yamaguchi Tadashi"]})

@app.route('/volleyballs')
def get_volleyballs():
    rows = execute("SELECT id, name, description FROM volleyball", fetch=True)
    volleyballs = [{"id": r[0], "name": r[1], "description": r[2]} for r in rows]
    return jsonify({"volleyballs": volleyballs})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)