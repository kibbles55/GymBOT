from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from states import ViewPlans
from crud import delete_user_plan, update_user_plans


async def select_plan_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: int):
    user_plans = manager.dialog_data.get('user_plans_data', {})
    plan = user_plans.get(int(item_id), {})
    manager.dialog_data['choice_user_plan'] = plan
    await manager.switch_to(ViewPlans.edit_plan)

async def delete_plan_handler(callback: CallbackQuery, widget, manager: DialogManager):
    plans = manager.dialog_data.get('choice_user_plan', {})
    plan_id = plans.get('id')
    user_id = manager.event.from_user.id
    await delete_user_plan(telegram_id=user_id, plan_id=plan_id)
    await manager.switch_to(ViewPlans.main)



async def delete_exercises_from_plan(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: int):
    plans = manager.dialog_data.get('choice_user_plan', {})
    day_schedule = plans.get("exercises", {})
    day_schedule.pop(item_id, None)
    plan_id = plans.get('id')
    new_exercises = day_schedule
    manager.dialog_data['choice_user_plan']['exercises'] = new_exercises
    #await update_user_plans(plan_id=plan_id, new_exercises=new_exercises)

    await manager.switch_to(ViewPlans.edit_plan)

async def muscle_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data["selected_muscle"] = item_id
    manager.dialog_data.pop("cached_exercises", None)
    await manager.switch_to(ViewPlans.add_exercises)


async def exercise_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: int):
    exercises = manager.dialog_data.get("cached_exercises", [])
    name = next((name for eid, name in exercises if eid == int(item_id)), item_id)
    plans = manager.dialog_data.get('choice_user_plan', {})
    day_schedule = plans.get("exercises", {})
    if item_id not in day_schedule:
        day_schedule[item_id] = name
        manager.dialog_data["exercises"] = day_schedule
        await callback.answer(f"✅ Вправу '{name}' додано до розкладу!")
    else:
        await callback.answer(f"⚠️ Вправа '{name}' вже є в розкладі!")

async def save_update_plan(callback: CallbackQuery, widget, manager: DialogManager, **kwargs):
    plans = manager.dialog_data.get('choice_user_plan', {})
    plan_id = plans.get('id')
    plan_name = plans.get("name")
    new_exercises = plans.get("exercises", {})

    await update_user_plans(plan_id, plan_name, new_exercises)
    await callback.answer("✅ План збережено!")
