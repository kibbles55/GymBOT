from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    main = State()

class CreatePlan(StatesGroup):
    main = State()
    muscle_choice = State()
    exercises = State()
    change_name = State()
    delete_exercises = State()

class ViewPlans(StatesGroup):
    main = State()
    delete_plan = State()
    edit_plan = State()
    chose_group = State()
    add_exercises = State()
    delete_exercises = State()

class Settings(StatesGroup):
    main = State()
    add_exercises = State()
    change_name = State()
    muscle_choice = State()


MUSCLE_GROUPS = [
    {"id": 1, "name": "Груди"},
    {"id": 2, "name": "Спина"},
    {"id": 3, "name": "Дельти"},
    {"id": 4, "name": "Трицепс"},
    {"id": 5, "name": "Біцепс"},
    {"id": 6, "name": "Ноги"},
    {"id": 7, "name": "Живіт"},
]
