import asyncio
import os
from aiogram import Bot, Dispatcher, types
from screenshot import make_screenshot, is_updated

TOKEN = os.getenv("8443606906:AAHJiInWJG8d1W7N0e67fj7-GSLIOWKZzQg")
CHAT_ID = int(os.getenv("737072371"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(commands=["test"])
async def test_cmd(message: types.Message):
    if message.chat.id != CHAT_ID:
        return
    make_screenshot()
    await bot.send_photo(
        CHAT_ID,
        photo=open("current.png", "rb"),
        caption="📊 Поточний графік відключень світла"
    )

async def checker():
    if is_updated():
        await bot.send_photo(
            CHAT_ID,
            photo=open("current.png", "rb"),
            caption="⚡ Оновився графік відключень світла"
        )

async def on_startup():
    make_screenshot()
    await bot.send_photo(
        CHAT_ID,
        photo=open("current.png", "rb"),
        caption="📊 Поточний графік (бот запущено)"
    )

async def main():
    await on_startup()
    asyncio.create_task(dp.start_polling(bot))
    while True:
        try:
            await checker()
        except Exception as e:
            print("ERROR:", e)
        await asyncio.sleep(1800)

asyncio.run(main())
