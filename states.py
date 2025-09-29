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

class Settings(StatesGroup):
    main = State()
    add_exercises = State()
    change_name = State()
    muscle_choice = State()
