from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Group, Select, Start
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from states import CreatePlan, MainMenu
from states import ViewPlans, MUSCLE_GROUPS
from crud import get_user_plans, get_exercises
from .handlers import select_plan_handler, delete_plan_handler, delete_exercises_from_plan, muscle_handler, exercise_handler, save_update_plan
import json

async def get_exercises_list(dialog_manager, **kwargs):
    if "cached_exercises" not in dialog_manager.dialog_data:
        selected_muscle = dialog_manager.dialog_data.get("selected_muscle")
        result = await get_exercises(selected_muscle)
        dialog_manager.dialog_data["cached_exercises"] = [(e.id, e.name) for e in result]
    return {"exercises": dialog_manager.dialog_data["cached_exercises"]}


async def get_user_plan(dialog_manager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    plans = await get_user_plans(telegram_id=user_id)

    plan_data = {}
    for plan in plans:
        exercises = plan.exercises
        if isinstance(exercises, str):
            exercises = json.loads(exercises)
        plan_data[plan.id] = {
            'id': plan.id,
            "name": plan.plan_name,
            "exercises": exercises
        }

    dialog_manager.dialog_data["user_plans_data"] = plan_data
    return {'user_plans': [(plan.id, plan.plan_name) for plan in plans]}

async def get_plan_info(dialog_manager, **kwargs):
    plan = dialog_manager.dialog_data.get("choice_user_plan", None)
    exercises = '\n'.join(plan['exercises'].values())
    exercises_list = [{"id": k, "name": v} for k, v in plan['exercises'].items()]
    return {"id": plan['id'], "name": plan['name'], "exercises": exercises, "exercises_list": exercises_list}




main_window = Window(
    Format("🏋️ <b>Список планів:</b>"),
    Group(
        Select(
            Format("📌 {item[1]}"),
            id="user_plans",
            item_id_getter=lambda x: x[0],
            items="user_plans",
            on_click=select_plan_handler,
        ),
        width=1,
    ),
    Start(Const("🏠 Повернутися в головне меню"), id="back_main", state=MainMenu.main),
    state=ViewPlans.main,
    getter=get_user_plan,
)

edit_plan_window = Window(
Format("🏋️ <b>Назва плану:</b> {name}"),
    Format("📋 <b>Вправи:</b>\n{exercises}"),
    SwitchTo(Const('➕ Додати вправу'), id='add_exercises', state=ViewPlans.chose_group),
    SwitchTo(Const('🗑 Видалити вправу'), id='delete_exercises', state=ViewPlans.delete_exercises),
    Button(Const('💾 Зберегти зміни'), id='update_plan', on_click=save_update_plan),
    Button(Const('❌ Видалити план'), id='delete_plan', on_click=delete_plan_handler),
    Start(Const("🏠 Повернутися в головне меню"), id="back_main", state=MainMenu.main),
    state=ViewPlans.edit_plan,
    getter=get_plan_info,
)

chose_group_window = Window(
    Const("💪 Оберіть групу м'язів:"),
    Group(
        Select(
            Format("🏷 {item[name]}"),
            id="muscle_select",
            items=MUSCLE_GROUPS,
            item_id_getter=lambda x: x['id'],
            on_click=muscle_handler,
        ),
        width=2,
    ),
    SwitchTo(Const("⬅ Назад"), id="back", state=ViewPlans.edit_plan),
    state=ViewPlans.chose_group,
)

add_exercises_window = Window(
    Const("🏋️ Оберіть вправу:"),
    Group(
        Select(
            Format("✅ {item[1]}"),
            id="exercise_select",
            item_id_getter=lambda x: x[0],
            items="exercises",
            on_click=exercise_handler,
        ),
        width=1,
    ),
    SwitchTo(Const("Назад"), id="back", state=ViewPlans.chose_group),
    state=ViewPlans.add_exercises,
    getter=get_exercises_list,
)
delete_exercises_window = Window(
    Const("🗑 Виберіть вправу для видалення:"),
    Group(Select(
        Format("❌ {item[name]}"),
        id="delete_from_user_plans",
        item_id_getter=lambda x: x['id'],
        items="exercises_list",
        on_click=delete_exercises_from_plan,

    ),
        width=1,
    ),
    SwitchTo(Const("⬅ Назад"), id="back_edit_plan", state=ViewPlans.edit_plan),
    state=ViewPlans.delete_exercises,
    getter=get_plan_info,
)


view_plan_dialog = Dialog(
    main_window,
    edit_plan_window,
    delete_exercises_window,
    chose_group_window,
    add_exercises_window,
)
