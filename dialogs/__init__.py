from .main_menu import main_menu_dialog
from .create_plan import create_plan_dialog
from .view_plan import view_plan_dialog
from .settings import settings_dialog


all_dialogs = [
    main_menu_dialog,
    create_plan_dialog,
    view_plan_dialog,
    settings_dialog,

]

def register_dialogs(dp):
    for dialog in all_dialogs:
        dp.include_router(dialog)
    from aiogram_dialog import setup_dialogs
    setup_dialogs(dp)
