import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            subscribed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def save_user(user):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, chat_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user.id,
        user.id,
        user.username,
        user.first_name,
        user.last_name
    ))
    conn.commit()
    conn.close()

def update_subscription(chat_id: int, subscribe: bool):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET subscribed = ? WHERE chat_id = ?", (1 if subscribe else 0, chat_id))
    conn.commit()
    conn.close()

def get_subscribed_chat_ids():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users WHERE subscribed = 1")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]
def get_all_users():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT chat_id, username FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows
