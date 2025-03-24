import sqlite3

def connect_db():
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs_channel (
            guild_id INTEGER PRIMARY KEY,
            channel_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

def set_logs_channel(guild_id, channel_id):
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs_channel (guild_id, channel_id) VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET channel_id = excluded.channel_id
    """, (guild_id, channel_id))
    conn.commit()
    conn.close()

def get_logs_channel(guild_id):
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM logs_channel WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
