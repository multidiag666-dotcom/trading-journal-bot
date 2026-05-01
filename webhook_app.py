import asyncio
from flask import Flask, jsonify, request, render_template
from database import init_db, add_trade, get_today_trades, get_all_trades, get_stats, delete_trade
from verify import verify_telegram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

app = Flask(__name__)

WEBHOOK_PATH = '/webhook'
BOT_TOKEN = '8278666246:AAG7oK_1ODMCagxo9XlDckUnhsvB7eX3iE8'
WEBAPP_URL = 'https://trading-journal-bot-dukr.onrender.com'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(msg: types.Message):
    menu_keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='📊 Открыть журнал')]], resize_keyboard=True)
    await msg.answer('👇 Откройте журнал:', reply_markup=menu_keyboard)

@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = types.Update(**request.json)
    await dp.feed_update(bot, update)
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trades', methods=['GET', 'POST'])
def api_trades():
    uid = verify_telegram()
    if request.method == 'POST':
        data = request.get_json()
        add_trade(uid, data)
        return jsonify({'status': 'ok'})
    else:
        return jsonify(get_all_trades(uid))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)