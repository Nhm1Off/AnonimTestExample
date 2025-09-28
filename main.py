from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio

TOKEN = "8491900645:AAGx-I6Ce9wwydgUPOOR7ka4Pzp6k_ttv5M"

bot = Bot(token=TOKEN)
dp = Dispatcher()

queue = []
active_chats = {}

# Клавиатуры для aiogram v3
menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔎 Найти собеседника")]
    ],
    resize_keyboard=True
)

chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Завершить чат")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Это анонимный чат 🤫\nНажми кнопку ниже, чтобы найти собеседника.",
        reply_markup=menu_kb
    )

@dp.message(lambda m: m.text == "🔎 Найти собеседника")
async def search_partner(message: types.Message):
    user_id = message.from_user.id
    if user_id in queue:
        await message.answer("Ты уже в очереди, подожди 🙃")
        return

    queue.append(user_id)
    await message.answer("Ты в очереди... ждем другого пользователя 👀")

    if len(queue) >= 2:
        user1 = queue.pop(0)
        user2 = queue.pop(0)
        active_chats[user1] = user2
        active_chats[user2] = user1

        await bot.send_message(user1, "🎉 Собеседник найден! Можешь начинать общение.", reply_markup=chat_kb)
        await bot.send_message(user2, "🎉 Собеседник найден! Можешь начинать общение.", reply_markup=chat_kb)

@dp.message(lambda m: m.text == "❌ Завершить чат")
async def end_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id not in active_chats:
        await message.answer("Ты сейчас ни с кем не общаешься.", reply_markup=menu_kb)
        return

    partner_id = active_chats[user_id]
    await bot.send_message(partner_id, "❌ Собеседник завершил чат.", reply_markup=menu_kb)
    await message.answer("❌ Ты завершил чат.", reply_markup=menu_kb)

    del active_chats[user_id]
    del active_chats[partner_id]

@dp.message()
async def relay_message(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        await bot.send_message(partner_id, message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
