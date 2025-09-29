from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const
from states import MainMenu, CreatePlan, ViewPlans, Settings



main_window = Window(
    Const("🏠 Головне меню:"),
    Start(Const("➕ Створити план"), id="create_plan", state=CreatePlan.main),
    Start(Const("📋 Переглянути плани"), id="view_plans", state=ViewPlans.main),
    Start(Const("⚙️ Налаштування"), id="settings", state=Settings.main),
    state=MainMenu.main,
)

main_menu_dialog = Dialog(main_window)
