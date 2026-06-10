#!/usr/bin/env python3
"""Learning Tracker REST API — SQLite backend"""

import sqlite3, base64, json, time, os, uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

DB_PATH = "/root/learning-tracker-api/tracker.db"
PORT = 5000

app = Flask(__name__)
CORS(app)

# Hard-coded users (password stored as plain text for this migration prototype)
USERS = {
    "scarlett": "Scarlett1234",
    "raylan":   "Raylan1234",
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_tracker_data (
            user_id      TEXT PRIMARY KEY,
            tasks        TEXT DEFAULT '[]',
            sessions     TEXT DEFAULT '{}',
            calendar_tasks TEXT DEFAULT '{}',
            countdowns   TEXT DEFAULT '[]',
            created_at   TEXT,
            updated_at   TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_tracker_profiles (
            user_id      TEXT PRIMARY KEY,
            username     TEXT UNIQUE NOT NULL,
            display_name TEXT,
            created_at   TEXT,
            updated_at   TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_tracker_pairs (
            id                 TEXT PRIMARY KEY,
            requester_id       TEXT NOT NULL,
            partner_id         TEXT NOT NULL,
            requester_username TEXT,
            partner_username   TEXT,
            status             TEXT NOT NULL DEFAULT 'pending',
            created_at         TEXT,
            updated_at         TEXT,
            UNIQUE(requester_id, partner_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_tracker_meta (
            key   TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pairs_requester_status
        ON learning_tracker_pairs(requester_id, status)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pairs_partner_status
        ON learning_tracker_pairs(partner_id, status)
    """)
    seed_profiles_and_pair(conn)
    conn.commit()
    conn.close()

def now_iso():
    return datetime.utcnow().isoformat()

def seed_profiles_and_pair(conn):
    now = now_iso()
    for username in USERS:
        display_name = "Raylan" if username == "raylan" else "Scarlett"
        conn.execute("""
            INSERT INTO learning_tracker_profiles (user_id, username, display_name, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                display_name = excluded.display_name,
                updated_at = excluded.updated_at
        """, (username, username, display_name, now, now))

    seeded = conn.execute(
        "SELECT value FROM learning_tracker_meta WHERE key = 'initial_pair_seeded'"
    ).fetchone()
    if not seeded:
        exists = conn.execute("""
            SELECT id FROM learning_tracker_pairs
            WHERE (requester_id = 'raylan' AND partner_id = 'scarlett')
               OR (requester_id = 'scarlett' AND partner_id = 'raylan')
            LIMIT 1
        """).fetchone()
        if not exists:
            conn.execute("""
                INSERT OR IGNORE INTO learning_tracker_pairs
                    (id, requester_id, partner_id, requester_username, partner_username, status, created_at, updated_at)
                VALUES (?, 'raylan', 'scarlett', 'raylan', 'scarlett', 'accepted', ?, ?)
            """, (str(uuid.uuid4()), now, now))
        conn.execute("""
            INSERT OR REPLACE INTO learning_tracker_meta (key, value)
            VALUES ('initial_pair_seeded', ?)
        """, (now,))

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if username not in USERS or USERS[username] != password:
        return jsonify({"error": "密码错误"}), 401

    token = base64.b64encode(f"{username}:{int(time.time())}".encode()).decode()
    return jsonify({"token": token, "user_id": username, "username": username})

# ---------------------------------------------------------------------------
# Data CRUD
# ---------------------------------------------------------------------------

def verify_token(req):
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    try:
        decoded = base64.b64decode(auth[7:].encode()).decode()
        username = decoded.split(":")[0]
        return username if username in USERS else None
    except Exception:
        return None

def require_user():
    user = verify_token(request)
    if not user:
        return None, (jsonify({"error": "未授权"}), 401)
    return user, None

def parse_eq_arg(name):
    value = request.args.get(name)
    if not value:
        return None
    return value[3:] if value.startswith("eq.") else value

def row_to_dict(row):
    return dict(row) if row else None

def parse_json_field(value, fallback):
    try:
        return json.loads(value if value else json.dumps(fallback))
    except Exception:
        return fallback

def serialize_data_row(row):
    result = dict(row)
    result["tasks"] = parse_json_field(result.get("tasks"), [])
    result["sessions"] = parse_json_field(result.get("sessions"), {})
    result["calendar_tasks"] = parse_json_field(result.get("calendar_tasks"), {})
    result["countdowns"] = parse_json_field(result.get("countdowns"), [])
    return result

def has_accepted_pair(conn, user_a, user_b):
    if user_a == user_b:
        return True
    row = conn.execute("""
        SELECT id FROM learning_tracker_pairs
        WHERE status = 'accepted'
          AND ((requester_id = ? AND partner_id = ?)
            OR (requester_id = ? AND partner_id = ?))
        LIMIT 1
    """, (user_a, user_b, user_b, user_a)).fetchone()
    return row is not None

@app.route("/api/data", methods=["GET"])
def get_data():
    user, error = require_user()
    if error:
        return error

    user_id = request.args.get("user_id", user)
    conn = get_db()
    if not has_accepted_pair(conn, user, user_id):
        conn.close()
        return jsonify({"error": "无权访问该用户数据"}), 403
    row = conn.execute(
        "SELECT * FROM learning_tracker_data WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "用户不存在"}), 404

    return jsonify(serialize_data_row(row))

@app.route("/api/data", methods=["POST"])
def save_data():
    user, error = require_user()
    if error:
        return error

    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", user)
    if user_id != user:
        return jsonify({"error": "禁止写入他人数据"}), 403

    tasks         = json.dumps(data.get("tasks", []), ensure_ascii=False)
    sessions      = json.dumps(data.get("sessions", {}), ensure_ascii=False)
    calendar_tasks = json.dumps(data.get("calendar_tasks", {}), ensure_ascii=False)
    countdowns    = json.dumps(data.get("countdowns", []), ensure_ascii=False)
    now           = now_iso()

    conn = get_db()
    conn.execute("""
        INSERT INTO learning_tracker_data (user_id, tasks, sessions, calendar_tasks, countdowns, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            tasks         = excluded.tasks,
            sessions      = excluded.sessions,
            calendar_tasks= excluded.calendar_tasks,
            countdowns    = excluded.countdowns,
            updated_at    = excluded.updated_at
    """, (user_id, tasks, sessions, calendar_tasks, countdowns, now, now))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# ---------------------------------------------------------------------------
# Supabase/PostgREST-compatible sharing endpoints
# ---------------------------------------------------------------------------

@app.route("/api/learning_tracker_profiles", methods=["GET"])
def list_profiles():
    user, error = require_user()
    if error:
        return error

    username = parse_eq_arg("username")
    user_id = parse_eq_arg("user_id")
    conn = get_db()
    if username:
        rows = conn.execute(
            "SELECT * FROM learning_tracker_profiles WHERE username = ? LIMIT 1",
            (username,),
        ).fetchall()
    elif user_id:
        rows = conn.execute(
            "SELECT * FROM learning_tracker_profiles WHERE user_id = ? LIMIT 1",
            (user_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM learning_tracker_profiles WHERE user_id = ?",
            (user,),
        ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/learning_tracker_profiles", methods=["POST"])
def upsert_profile():
    user, error = require_user()
    if error:
        return error

    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", user)
    if user_id != user:
        return jsonify({"error": "禁止写入他人档案"}), 403

    username = (data.get("username") or user).strip()
    display_name = data.get("display_name")
    now = now_iso()
    conn = get_db()
    conn.execute("""
        INSERT INTO learning_tracker_profiles (user_id, username, display_name, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            display_name = excluded.display_name,
            updated_at = excluded.updated_at
    """, (user_id, username, display_name, now, now))
    row = conn.execute(
        "SELECT * FROM learning_tracker_profiles WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.commit()
    conn.close()
    return jsonify([dict(row)])

@app.route("/api/learning_tracker_pairs", methods=["GET"])
def list_pairs():
    user, error = require_user()
    if error:
        return error

    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM learning_tracker_pairs
        WHERE requester_id = ? OR partner_id = ?
        ORDER BY created_at DESC
    """, (user, user)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/learning_tracker_pairs", methods=["POST"])
def create_pair():
    user, error = require_user()
    if error:
        return error

    data = request.get_json(silent=True) or {}
    requester_id = data.get("requester_id", user)
    partner_id = data.get("partner_id")
    if requester_id != user:
        return jsonify({"error": "禁止代他人发起关联"}), 403
    if not partner_id or partner_id == user:
        return jsonify({"error": "关联对象无效"}), 400

    now = now_iso()
    conn = get_db()
    partner = conn.execute(
        "SELECT * FROM learning_tracker_profiles WHERE user_id = ?",
        (partner_id,),
    ).fetchone()
    if not partner:
        conn.close()
        return jsonify({"error": "关联对象不存在"}), 404

    existing = conn.execute("""
        SELECT * FROM learning_tracker_pairs
        WHERE (requester_id = ? AND partner_id = ?)
           OR (requester_id = ? AND partner_id = ?)
        ORDER BY created_at DESC
        LIMIT 1
    """, (user, partner_id, partner_id, user)).fetchone()
    if existing:
        conn.close()
        return jsonify([dict(existing)])

    pair_id = str(uuid.uuid4())
    conn.execute("""
        INSERT INTO learning_tracker_pairs
            (id, requester_id, partner_id, requester_username, partner_username, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
    """, (
        pair_id,
        user,
        partner_id,
        data.get("requester_username", user),
        data.get("partner_username", partner["username"]),
        now,
        now,
    ))
    row = conn.execute("SELECT * FROM learning_tracker_pairs WHERE id = ?", (pair_id,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify([dict(row)])

@app.route("/api/learning_tracker_pairs", methods=["PATCH"])
def update_pair():
    user, error = require_user()
    if error:
        return error

    pair_id = parse_eq_arg("id")
    status = (request.get_json(silent=True) or {}).get("status")
    if not pair_id or status not in ("pending", "accepted", "rejected"):
        return jsonify({"error": "请求无效"}), 400

    conn = get_db()
    pair = conn.execute(
        "SELECT * FROM learning_tracker_pairs WHERE id = ?",
        (pair_id,),
    ).fetchone()
    if not pair:
        conn.close()
        return jsonify({"error": "关联不存在"}), 404
    if user not in (pair["requester_id"], pair["partner_id"]):
        conn.close()
        return jsonify({"error": "无权修改该关联"}), 403

    conn.execute(
        "UPDATE learning_tracker_pairs SET status = ?, updated_at = ? WHERE id = ?",
        (status, now_iso(), pair_id),
    )
    row = conn.execute("SELECT * FROM learning_tracker_pairs WHERE id = ?", (pair_id,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify([dict(row)])

@app.route("/api/learning_tracker_pairs", methods=["DELETE"])
def delete_pair():
    user, error = require_user()
    if error:
        return error

    pair_id = parse_eq_arg("id")
    if not pair_id:
        return jsonify({"error": "请求无效"}), 400

    conn = get_db()
    pair = conn.execute(
        "SELECT * FROM learning_tracker_pairs WHERE id = ?",
        (pair_id,),
    ).fetchone()
    if not pair:
        conn.close()
        return jsonify({"error": "关联不存在"}), 404
    if user not in (pair["requester_id"], pair["partner_id"]):
        conn.close()
        return jsonify({"error": "无权删除该关联"}), 403

    conn.execute("DELETE FROM learning_tracker_pairs WHERE id = ?", (pair_id,))
    conn.commit()
    conn.close()
    return ("", 204)

@app.route("/api/learning_tracker_data", methods=["GET"])
def list_learning_tracker_data():
    user, error = require_user()
    if error:
        return error

    target = parse_eq_arg("user_id") or user
    conn = get_db()
    if not has_accepted_pair(conn, user, target):
        conn.close()
        return jsonify({"error": "无权访问该用户数据"}), 403

    row = conn.execute(
        "SELECT * FROM learning_tracker_data WHERE user_id = ?",
        (target,),
    ).fetchone()
    conn.close()
    return jsonify([serialize_data_row(row)] if row else [])

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT, debug=False)
