from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Group, Select, Start
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from states import CreatePlan, MainMenu, MUSCLE_GROUPS
from .handlers import (
    save_user_plan, clean_plan_exercises, save_training_name,
    delete_exercises_from_plan, muscle_handler, exercise_handler,
)
from crud import get_exercises


async def get_plan_exercises(dialog_manager, **kwargs):
    exercises = dialog_manager.dialog_data.get("day_schedule", {})
    plan_name = dialog_manager.dialog_data.get("plan_name", "НЕ ВСТАНОВЛЕНО")
    exercise_list_text = "\n".join(
        [f"{i}. {name}" for i, (eid, name) in enumerate(exercises.items(), start=1)]
    ) or "Список порожній"
    return {
        "plan_name": plan_name,
        "exercise_list": exercise_list_text,
        "exercises_for_select": list(exercises.items()),
    }


async def get_exercises_list(dialog_manager, **kwargs):
    if "cached_exercises" not in dialog_manager.dialog_data:
        selected_muscle = dialog_manager.dialog_data.get("selected_muscle")
        result = await get_exercises(selected_muscle)
        dialog_manager.dialog_data["cached_exercises"] = [(e.id, e.name) for e in result]
    return {"exercises": dialog_manager.dialog_data["cached_exercises"]}



main_window = Window(
    Format("🏋️ <b>Назва плану:</b> {plan_name}"),
    Format("📋 <b>Вправи:\n{exercise_list}</b>"),
    SwitchTo(Const("➕ Додати вправу"), id="add_exercise", state=CreatePlan.muscle_choice),
    SwitchTo(Const("🗑 Видалити вправу"), id="delete_exercise", state=CreatePlan.delete_exercises),
    SwitchTo(Const("✏️ Змінити назву"), id="change_name", state=CreatePlan.change_name),
    Button(Const("🧹 Очистити"), id="clean_plan", on_click=clean_plan_exercises),
    Button(Const("💾 Зберегти"), id="save_plan", on_click=save_user_plan),
    Start(Const("🏠 Повернутися в головне меню"), id="back_main", state=MainMenu.main),
    state=CreatePlan.main,
    getter=get_plan_exercises,
)

delete_window = Window(
    Const("Оберіть вправу для видалення:"),
    Group(
        Select(
            Format("{item[1]}"),
            id="delete_select",
            item_id_getter=lambda x: x[0],
            items="exercises_for_select",
            on_click=delete_exercises_from_plan,
        ),
        width=1,
    ),
    SwitchTo(Const("Назад"), id="back", state=CreatePlan.main),
    state=CreatePlan.delete_exercises,
    getter=get_plan_exercises,
)

change_name_window = Window(
    Const("Введіть нову назву плану:"),
    TextInput(id="plan_name_input", on_success=save_training_name),
    SwitchTo(Const("Відмінити"), id="cancel", state=CreatePlan.main),
    state=CreatePlan.change_name,
)

muscle_window = Window(
    Const("Оберіть групу м'язів:"),
    Group(
        Select(
            Format("{item[name]}"),
            id="muscle_select",
            items=MUSCLE_GROUPS,
            item_id_getter=lambda x: x['id'],
            on_click=muscle_handler,
        ),
        width=2,
    ),
    SwitchTo(Const("Назад"), id="back", state=CreatePlan.main),
    state=CreatePlan.muscle_choice,
)

exercises_window = Window(
    Const("Оберіть вправу:"),
    Group(
        Select(
            Format("{item[1]}"),
            id="exercise_select",
            item_id_getter=lambda x: x[0],
            items="exercises",
            on_click=exercise_handler,
        ),
        width=1,
    ),
    SwitchTo(Const("Назад"), id="back", state=CreatePlan.muscle_choice),
    state=CreatePlan.exercises,
    getter=get_exercises_list,
)


create_plan_dialog = Dialog(
    main_window,
    delete_window,
    change_name_window,
    muscle_window,
    exercises_window,
)
