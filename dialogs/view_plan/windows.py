from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Group, Select, Start
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from states import CreatePlan, MainMenu
from states import ViewPlans
from crud import get_user_plans
from .handlers import select_plan_handler, delete_plan_handler
import json

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
    print('log')
    exercises = '\n'.join(plan['exercises'].values())
    return {"id": plan['id'], "name": plan['name'], "exercises": exercises}




main_window = Window(
    Format("🏋️ <b>Список планів:</b>"),
    Group(
        Select(
            Format("{item[1]}"),
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
Format("🏋️ <b>Назва {name}:</b>"),
    Format("🏋️ <b>Вправи: \n {exercises}:</b>"),
    Button(Const('Видалити план'), id='delete_plan', on_click=delete_plan_handler),
    Start(Const("🏠 Повернутися в головне меню"), id="back_main", state=MainMenu.main),
    state=ViewPlans.edit_plan,
    getter=get_plan_info,
)



view_plan_dialog = Dialog(
    main_window,
    edit_plan_window,
)