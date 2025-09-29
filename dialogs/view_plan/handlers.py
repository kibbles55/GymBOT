from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from states import ViewPlans
from crud import delete_user_plan



async def select_plan_handler(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: int):
    user_plans = manager.dialog_data.get('user_plans_data', {})
    plan = user_plans.get(int(item_id), {})
    manager.dialog_data['choice_user_plan'] = plan
    await manager.switch_to(ViewPlans.edit_plan)

async def delete_plan_handler(callback: CallbackQuery, widget: Select, manager: DialogManager):
    plans = manager.dialog_data.get('choice_user_plan', {})
    plan_id = plans.get('id')
    user_id = manager.event.from_user.id
    await delete_user_plan(telegram_id=user_id, plan_id=plan_id)
    await manager.switch_to(ViewPlans.main)
