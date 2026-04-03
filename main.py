import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
TOKEN = "8651984688:AAGiWSHa3Of5vE4lOg92mM5URRwlWQwCFLQ"
CHANNEL_ID = "@happkluchi"
# Твоя ссылка, где прописано 1000 GB
CONFIG_URL = "https://pastebin.com/raw/WAgbRiKi"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРА ---
def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔑 Получить ключ", callback_data="get_key")]
    ])

def sub_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_ID[1:]}")],
        [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="get_key")]
    ])

# --- ЛОГИКА ---
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Ты в **RV BOT**.\n\nНажми кнопку ниже, чтобы получить доступ к VPN.",
        reply_markup=main_kb()
    )

@dp.callback_query(F.data == "get_key")
async def send_key(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id):
        text = (
            "✅ **Доступ разрешен!**\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "📊 **Лимит:** `1000 GB` (Premium)\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "👇 **Инструкция:**\n"
            "1. Скопируй ссылку ниже.\n"
            "2. В приложении **Happ** нажми **+**.\n"
            "3. Выбери **Добавить подписку** (URL).\n"
            "4. Вставь ссылку и нажми **Обновить** (🔄).\n\n"
            f"`{CONFIG_URL}`"
        )
        # Используем edit_text для скорости, чтобы не плодить сообщения
        await call.message.edit_text(text, parse_mode="Markdown")
    else:
        await call.answer("❌ Вы не подписаны!", show_alert=True)
        await call.message.edit_text(
            "⚠️ Для получения ключа нужно подписаться на наш канал.",
            reply_markup=sub_kb()
        )

async def main():
    print("Бот запущен в лайт-режиме!")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
  
