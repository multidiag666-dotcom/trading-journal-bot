import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = '8278666246:AAG7oK_1ODMCagxo9XlDckUnhsvB7eX3iE8'

# ⚠️ ЗАМЕНИ ЭТУ СТРОКУ ПОСЛЕ ДЕПЛОЯ НА РЕАЛЬНЫЙ HTTPS-АДРЕС РЕНДЕРА
WEBAPP_URL = 'https://твой-сервис.onrender.com'   # ВРЕМЕННО ТАК, ПОТОМ ЗАМЕНИ

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
        '🎓 Добро пожаловать в журнал трейдера\n'
        'Академии «Успешный трейдер»\n\n'
        'Здесь вы фиксируете сделки и анализируете результаты.\n\n'
        '👇 Откройте журнал:',
        reply_markup=menu_keyboard
    )

@dp.message(lambda m: m.text == '📊 Открыть журнал')
async def open_journal(msg: types.Message):
    await msg.answer('Нажмите кнопку ниже, чтобы открыть журнал:',
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=[[types.KeyboardButton(text='Открыть журнал',
                                                          web_app=types.WebAppInfo(url=WEBAPP_URL))]],
                         resize_keyboard=True
                     ))

@dp.message(lambda m: m.text == '📈 Моя статистика')
async def stats_command(msg: types.Message):
    from database import get_stats
    s = get_stats(msg.from_user.id)
    text = (f"📊 Статистика:\n"
            f"Всего сделок: {s['total']}\n"
            f"Winrate: {s['winrate']}%\n"
            f"✅ Плюсы: {s['plus']}   ❌ Минусы: {s['minus']}")
    await msg.answer(text, reply_markup=menu_keyboard)

@dp.message(lambda m: m.text == '📒 История')
async def history_command(msg: types.Message):
    from database import get_all_trades
    trades = get_all_trades(msg.from_user.id, limit=5)
    if not trades:
        await msg.answer('У вас пока нет записей.', reply_markup=menu_keyboard)
        return
    lines = []
    for t in trades:
        emoji = '🟢' if t['result'] == 'plus' else '🔴'
        lines.append(f"{emoji} {t['date']} | {t['asset']} | {t['direction']} | {t['result']}")
    await msg.answer('📒 Последние сделки:\n' + '\n'.join(lines), reply_markup=menu_keyboard)

@dp.message(lambda m: m.text == 'ℹ️ Как вести дневник')
async def help_cmd(msg: types.Message):
    await msg.answer(
        '📘 Правила ведения дневника:\n\n'
        '1️⃣ Перед входом записывай чёткую причину.\n'
        '2️⃣ После закрытия сделки пиши комментарий.\n'
        '3️⃣ Анализируй статистику раз в неделю.\n\n'
        'Системный подход = стабильный рост 🚀',
        reply_markup=menu_keyboard
    )

async def run_bot():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(run_bot())