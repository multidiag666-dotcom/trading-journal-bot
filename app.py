import asyncio
from flask import Flask, jsonify, request, render_template
from database import init_db, add_trade, get_today_trades, get_all_trades, get_stats, delete_trade
from verify import verify_telegram
from bot_dispatcher import dp, bot
from aiogram import types

app = Flask(__name__)

WEBHOOK_PATH = '/webhook'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/today')
def api_today():
    uid = verify_telegram()
    return jsonify(get_today_trades(uid))

@app.route('/api/trades', methods=['GET', 'POST'])
def api_trades():
    uid = verify_telegram()
    if request.method == 'POST':
        data = request.get_json()
        required = ['date','asset','entry_time','direction','volume','risk','result']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing fields'}), 400
        add_trade(uid, data)
        return jsonify({'status': 'ok'})
    else:
        return jsonify(get_all_trades(uid))

@app.route('/api/trades/<int:trade_id>', methods=['DELETE'])
def api_delete_trade(trade_id):
    uid = verify_telegram()
    deleted = delete_trade(trade_id, uid)
    if deleted:
        return jsonify({'status': 'deleted'})
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/api/stats')
def api_stats():
    uid = verify_telegram()
    return jsonify(get_stats(uid))

@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update_data = request.get_json()
    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=False)