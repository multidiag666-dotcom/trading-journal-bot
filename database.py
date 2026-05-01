import sqlite3
from datetime import date

DB = 'journal.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            asset TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            direction TEXT NOT NULL,
            volume REAL NOT NULL,
            risk REAL NOT NULL,
            entry_reason TEXT,
            after_comment TEXT,
            result TEXT NOT NULL
        )''')
        conn.commit()

def add_trade(user_id, data):
    with sqlite3.connect(DB) as conn:
        conn.execute('''INSERT INTO trades 
                        (user_id, date, asset, entry_time, direction, volume, risk, entry_reason, after_comment, result)
                        VALUES (?,?,?,?,?,?,?,?,?,?)''',
                     (user_id, data['date'], data['asset'], data['entry_time'],
                      data['direction'], data['volume'], data['risk'],
                      data.get('entry_reason', ''), data.get('after_comment', ''),
                      data['result']))
        conn.commit()

def get_today_trades(user_id):
    today = str(date.today())
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('SELECT * FROM trades WHERE user_id=? AND date=? ORDER BY id DESC', 
                          (user_id, today))
        columns = [col[0] for col in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def get_all_trades(user_id, limit=50):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('SELECT * FROM trades WHERE user_id=? ORDER BY id DESC LIMIT ?', 
                          (user_id, limit))
        columns = [col[0] for col in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def get_stats(user_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('SELECT result, COUNT(*) FROM trades WHERE user_id=? GROUP BY result', 
                          (user_id,))
        rows = cur.fetchall()
    
    total = sum(cnt for _, cnt in rows)
    plus = next((cnt for res, cnt in rows if res == 'plus'), 0)
    minus = next((cnt for res, cnt in rows if res == 'minus'), 0)
    winrate = round(plus / total * 100, 1) if total else 0
    
    return {'total': total, 'plus': plus, 'minus': minus, 'winrate': winrate}

def delete_trade(trade_id, user_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('DELETE FROM trades WHERE id=? AND user_id=?', (trade_id, user_id))
        conn.commit()
        return cur.rowcount  # 1 если удалено, 0 если не найдено