from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import async_session
from crud import get_user, update_user_weight, update_user_height
from aiogram.fsm.context import FSMContext


router = Router()

class Account(StatesGroup):
    edit_field = State()

def get_account_keyboard(user):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"⚖️ Змінити вагу ({user.weight or '-' } кг)", callback_data="update_weight")],
            [InlineKeyboardButton(text=f"📏 Змінити зріст ({user.height or '-' } см)", callback_data="update_height")],
        ]
    )


def format_weight(user):
    if user.weight is None:
        return "-"

    if user.old_weight is not None:
        diff = abs(user.weight - user.old_weight)
        emoji = "📈" if user.weight < user.old_weight else "📉"
        sign = "+" if user.weight > user.old_weight else "-"
        return f"<b>{user.weight} кг</b> {emoji} ({sign}{diff:.1f})"
    else:
        return f"<b>{user.weight} кг</b>"


@router.message(Command("settings"))
async def settings_handler(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("⚠️ У тебе ще немає акаунта.\nВикористай /start щоб створити профіль.")
        return

    text_weight = format_weight(user)

    text = (
        "⚙️ <b>Налаштування акаунта:</b>\n\n"
        f"⚖️ Вага: <b>{text_weight}</b> кг\n"
        f"📏 Зріст: <b>{user.height or '-'}</b> см\n"
        f"🕒 Оновлено: {user.updated_at.strftime('%d.%m.%Y %H:%M') if user.updated_at else '-'}"
    )
    await message.answer(text, reply_markup=get_account_keyboard(user))

@router.callback_query(F.data.in_({'update_weight', 'update_height'}))
async def edit_account_callback(callback: CallbackQuery, state: FSMContext):
    field = callback.data
    await state.update_data(editing_field=field)
    prompt = "Введіть вагу:" if field == "update_weight" else "Введіть зріст в см:"
    await callback.message.answer(prompt)
    await state.set_state(Account.edit_field)
    await callback.answer()


@router.message(Account.edit_field)
async def update_weight_state(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("editing_field")
    try:
        new_value = float(message.text)
    except ValueError:
        await message.answer("⚠️ Введіть число")
        return

    telegram_id = message.from_user.id

    if field == "update_weight":
        user = await update_user_weight(telegram_id, new_value)
        await message.answer(f"✅ Вага оновлена: <b>{new_value} кг</b>")
    elif field == "update_height":
        user = await update_user_height(telegram_id, new_value)
        await message.answer(f"✅ Зріст оновлено: <b>{new_value} см</b>")

    text_weight = format_weight(user)

    text = (
        "⚙️ <b>Налаштування акаунта:</b>\n\n"
        f"🏋️ Вага: {text_weight}\n"
        f"📏 Зріст: <b>{user.height or '-'} см</b>\n"
        f"🕒 Оновлено: {user.updated_at.strftime('%d.%m.%Y %H:%M') if user.updated_at else '-'}"
    )

    await message.answer(text, reply_markup=get_account_keyboard(user))
    await state.clear()


def register_handlers(dp):
    dp.include_router(router)
