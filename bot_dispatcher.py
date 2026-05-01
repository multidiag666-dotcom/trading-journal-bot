import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = '8278666246:AAG7oK_1ODMCagxo9XlDckUnhsvB7eX3iE8'          
WEBAPP_URL = 'https://trading-journal-bot-dukr.onrender.com'       

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='📊 Открыть журнал', web_app=types.WebAppInfo(url=WEBAPP_URL))],
        [types.KeyboardButton(text='📈 Моя статистика'), types.KeyboardButton(text='📒 История')],
        [types.KeyboardButton(text='ℹ️ Как вести дневник')]
    ],
    resize_keyboard=True
)

@dp.message(Command('start'))
async def start(msg: types.Message):
    await msg.answer(
        '🎓 Добро пожаловать в журнал трейдера\nАкадемии «Успешный трейдер»\n\n👇 Откройте журнал:',
        reply_markup=menu_keyboard
    )

@dp.message(lambda m: m.text == '📊 Открыть журнал')
async def open_journal(msg: types.Message):
    await msg.answer('Нажмите кнопку ниже:',
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=[[types.KeyboardButton(text='Открыть журнал',
                                                          web_app=types.WebAppInfo(url=WEBAPP_URL))]],
                         resize_keyboard=True
                     ))

@dp.message(lambda m: m.text == '📈 Моя статистика')
async def stats_command(msg: types.Message):
    from database import get_stats
    s = get_stats(msg.from_user.id)
    text = (f"📊 Статистика:\nВсего: {s['total']}\nWinrate: {s['winrate']}%\n✅ {s['plus']}   ❌ {s['minus']}")
    await msg.answer(text, reply_markup=menu_keyboard)

@dp.message(lambda m: m.text == '📒 История')
async def history_command(msg: types.Message):
    from database import get_all_trades
    trades = get_all_trades(msg.from_user.id, limit=5)
    if not trades:
        await msg.answer('Нет сделок.', reply_markup=menu_keyboard)
        return
    lines = [f"{'🟢' if t['result']=='plus' else '🔴'} {t['date']} {t['asset']} {t['result']}" for t in trades]
    await msg.answer('📒 Последние сделки:\n' + '\n'.join(lines), reply_markup=menu_keyboard)

@dp.message(lambda m: m.text == 'ℹ️ Как вести дневник')
async def help_cmd(msg: types.Message):
    await msg.answer(
        '📘 Правила:\n1. Причина входа\n2. Комментарий после\n3. Анализ статистики\n\nСистемный подход = рост 🚀',
        reply_markup=menu_keyboard
    )