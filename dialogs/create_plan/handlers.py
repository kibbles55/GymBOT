from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select
from crud import get_exercises, create_user_plan
from states import CreatePlan



async def save_user_plan(callback: CallbackQuery, widget, manager: DialogManager, **kwargs):
    plan_name = manager.dialog_data.get("plan_name")
    exercises = manager.dialog_data.get("day_schedule", {})
    user_id = callback.from_user.id

    saved = await create_user_plan(user_id, plan_name, exercises)
    if not saved:
        await callback.answer("⚠️ План з такою назвою вже існує!")
    else:
        await callback.answer("✅ План збережено!")


async def clean_plan_exercises(callback: CallbackQuery, widget, manager: DialogManager, **kwargs):
    manager.dialog_data["day_schedule"] = {}
    await callback.answer("План очищено!")
    await manager.switch_to(CreatePlan.main)


async def save_training_name(callback: CallbackQuery, widget: ManagedTextInput, manager: DialogManager, text: str, **kwargs):
    manager.dialog_data["plan_name"] = text
    await manager.switch_to(CreatePlan.main)
    await callback.answer(f"Назва плану встановлена: {text}")


async def delete_exercises_from_plan(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id):
    exercises = manager.dialog_data.get("day_schedule", {})
    exercises.pop(item_id, None)
    manager.dialog_data["day_schedule"] = exercises
    await callback.answer("Вправа видалена!")
    await manager.switch_to(CreatePlan.delete_exercises)


async def muscle_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data["selected_muscle"] = item_id
    manager.dialog_data.pop("cached_exercises", None)
    await manager.switch_to(CreatePlan.exercises)


async def exercise_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: int):
    exercises = manager.dialog_data.get("cached_exercises", [])
    name = next((name for eid, name in exercises if eid == int(item_id)), item_id)
    day_schedule = manager.dialog_data.get("day_schedule", {})
    if item_id not in day_schedule:
        day_schedule[item_id] = name
        manager.dialog_data["day_schedule"] = day_schedule
        await callback.answer(f"✅ Вправу '{name}' додано до розкладу!")
    else:
        await callback.answer(f"⚠️ Вправа '{name}' вже є в розкладі!")
