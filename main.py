import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from crud import get_user, update_user_weight
from database.models import User, WeightLog
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from database.database import async_session
import os
from dotenv import load_dotenv
from handlers import account

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


account.register_handlers(dp)

from dialogs import register_dialogs
from dialogs.main_menu import MainMenu

register_dialogs(dp)

@dp.message(Command("menu"))
async def menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.main, mode=StartMode.RESET_STACK)


@dp.message(Command("start"))
async def send_welcome(message: Message):
    user_id = int(message.from_user.id)
    user = await get_user(user_id)
    if user:
        await message.answer(
            "👋 Твій профіль вже є в базі!\n\n"
            "⚙️ Щоб оновити дані або додати вагу/зріст, заходь в налаштування: /settings\n\n"
            "📋 Використовуй /menu, щоб скористатися всіма можливостями бота."
        )
    else:
        async with async_session() as session:
            new_user = User(telegram_id=user_id)
            session.add(new_user)
            await session.commit()
            await message.answer(
                "🎉 Вітаю тебе в GymBro! 💪\n\n"
                "📏 Ти можеш відслідковувати свою вагу та зріст.\n"
                "⚙️ Щоб почати, заходь в налаштування: /settings\n\n"
                "📋 Використовуй /menu, щоб відкрити всі можливості бота."
            )




if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))