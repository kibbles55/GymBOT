from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select
from crud import get_exercises, create_user_plan, create_user_exercise
from states import Settings

async def save_exercises_name(callback: CallbackQuery, widget: ManagedTextInput, manager: DialogManager, text: str, **kwargs):
    manager.dialog_data["exercises_name"] = text
    await manager.switch_to(Settings.add_exercises)
    await callback.answer(f"Назва вправи встановлена: {text}")


async def muscle_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: int):
    manager.dialog_data["muscle_group"] = item_id
    await manager.switch_to(Settings.add_exercises)


async def save_user_exercises(callback: CallbackQuery, widget: Select, manager: DialogManager):
    user_id = manager.event.from_user.id
    exercises_name = manager.dialog_data.get("exercises_name")
    muscle_group = manager.dialog_data.get("muscle_group")
    if not exercises_name or not muscle_group:
        await callback.answer("Будь ласка, заповніть назву та групу м'язів")
        return
    result = await create_user_exercise(user_id, exercises_name, int(muscle_group))
    if result:
        manager.dialog_data.pop("exercises_name", None)
        manager.dialog_data.pop("muscle_group_id", None)

        await callback.answer(f"✅ Вправа '{exercises_name}' додана!")
        await manager.switch_to(Settings.main)



