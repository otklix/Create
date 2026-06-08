import os
import uuid
import base64
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
PLAYER_URL = "https://r18520082-design.github.io/Player/"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🔴 Отправь короткое голосовое или аудио")

@dp.message(lambda m: m.voice or m.audio)
async def handle(m: types.Message):
    snd = m.voice or m.audio
    mime = "audio/ogg" if m.voice else "audio/mpeg"
    
    if snd.file_size > 100000:
        await m.answer("❌ Слишком большой (>100 КБ)")
        return
    
    file = await bot.get_file(snd.file_id)
    data = (await bot.download_file(file.file_path)).getvalue()
    b64 = base64.b64encode(data).decode()
    link = f"{PLAYER_URL}?url=data:{mime};base64,{b64}"
    
    await m.answer(f"Ссылка для NFC:\n{link}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())