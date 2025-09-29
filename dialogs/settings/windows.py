from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Group, Select, Start
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from states import Settings, MainMenu
from .handlers import save_exercises_name, muscle_handler, save_user_exercises

MUSCLE_GROUPS = [
    {"id": 1, "name": "Груди"},
    {"id": 2, "name": "Спина"},
    {"id": 3, "name": "Дельти"},
    {"id": 4, "name": "Трицепс"},
    {"id": 5, "name": "Біцепс"},
    {"id": 6, "name": "Ноги"},
    {"id": 7, "name": "Живіт"},
]


async def get_exercise_info(dialog_manager, **kwargs):
    exercises_name = dialog_manager.dialog_data.get("exercises_name", "Не вказано")
    muscle_id = dialog_manager.dialog_data.get("muscle_group")
    muscle_group = (
        next((g["name"] for g in MUSCLE_GROUPS if g["id"] == int(muscle_id)), "Не вказано")
        if muscle_id is not None else "Не вказано"
    )
    return {
        "exercises_name": exercises_name,
        "muscle_group": muscle_group,
    }


main_window = Window(
    Format("🏋️ <b>Налаштування:</b>"),
    SwitchTo(Const('➕ Додати власну вправу'), id='add_user_exercises', state=Settings.add_exercises),

    Start(Const("🏠 Повернутися в головне меню"), id="back_main", state=MainMenu.main),
    state=Settings.main,
)


add_user_exercises_window = Window(
    Format("📛 Назва: {exercises_name}"),
    Format("💪 Група м'язів: {muscle_group}"),
    SwitchTo(Const("✏️ Задати ім'я"), id='change_name', state=Settings.change_name),
    SwitchTo(Const("💪 Задати групу м'язів"), id='change_muscle_group', state=Settings.muscle_choice),
    Button(Const("✅ Зберегти"), id='save_user_exercises', on_click=save_user_exercises),
    SwitchTo(Const("↩️ Назад"), id='back_to_main', state=Settings.main),
    state=Settings.add_exercises,
    getter=get_exercise_info,

)

change_name_window = Window(
    Const("Введіть назву вправи:"),
    TextInput(id="exercises_name_input", on_success=save_exercises_name),
    SwitchTo(Const("Відмінити"), id="cancel", state=Settings.main),
    state=Settings.change_name,
)

muscle_group_window = Window(
    Const("💪 Оберіть групу м'язів:"),
    Group(
        Select(
            Format("{item[name]}"),
            id="group_select",
            items=MUSCLE_GROUPS,
            item_id_getter=lambda x: x['id'],
            on_click=muscle_handler,
        ),
        width=2,
    ),
    SwitchTo(Const("↩️ Назад"), id="back", state=Settings.add_exercises),
    state=Settings.muscle_choice,
)

settings_dialog = Dialog(
    main_window,
    add_user_exercises_window,
    change_name_window,
    muscle_group_window
)