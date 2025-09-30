from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User, WeightLog, Exercise, UserExercise, MuscleGroup, UserPlan
from database.database import async_session
import json
from functools import wraps
from sqlalchemy import delete, and_


def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper

@with_session
async def get_user_plans(telegram_id: int, session: AsyncSession):
    user = await get_user(telegram_id)
    result = await session.execute(select(UserPlan).where(UserPlan.user_id == user.id))
    return result.scalars().all()

@with_session
async def update_user_plans(plan_id, plan_name, new_exercises, session: AsyncSession):
    result = await session.execute(select(UserPlan).where(and_(UserPlan.id == plan_id)))
    user_plan = result.scalars().first()
    if user_plan.plan_name != plan_name:
        user_plan.plan_name = plan_name
    user_plan.exercises = json.dumps(new_exercises, ensure_ascii=False)
    await session.commit()

@with_session
async def create_user_plan(telegram_id: int, plan_name: str, exercises: dict, session: AsyncSession):
    user = await get_user(telegram_id)
    existing = await session.execute(
        select(UserPlan)
        .where(UserPlan.user_id == user.id)
        .where(UserPlan.plan_name == plan_name)
    )
    existing_plan = existing.first()
    if existing_plan:
        return False

    user_plan = UserPlan(
        user_id=user.id,
        plan_name=plan_name,
        exercises=json.dumps(exercises, ensure_ascii=False)
    )
    session.add(user_plan)
    await session.commit()
    return True

@with_session
async def create_user_exercise(telegram_id: int, exercise_name: str, muscle_id:int, session: AsyncSession):
    user_exercise = UserExercise(user_id=telegram_id, muscle_id=muscle_id, name=exercise_name)
    session.add(user_exercise)
    await session.commit()
    return True

@with_session
async def delete_user_plan(telegram_id: int, session: AsyncSession, plan_id: int):
    user = await get_user(telegram_id)
    print(user.id)
    await session.execute(delete(UserPlan).where(and_(UserPlan.user_id == user.id, UserPlan.id == plan_id)))
    await session.commit()

@with_session
async def get_user(telegram_id, session: AsyncSession):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()

@with_session
async def update_user_weight(telegram_id, weight: float, session: AsyncSession):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()
    old_weight = user.weight or 0
    user.old_weight = old_weight
    user.weight = weight

    weight_log = WeightLog(user_id=user.id, weight=weight)
    session.add(weight_log)

    await session.commit()
    await session.refresh(user)
    return user


@with_session
async def update_user_height(telegram_id, height, session: AsyncSession):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()
    user.height = height
    await session.commit()
    await session.refresh(user)
    return user


@with_session
async def get_exercises(selected_muscle, session: AsyncSession):
    result = await session.execute(select(Exercise).where(Exercise.muscle_id == selected_muscle))
    base_exercises = result.scalars().all()
    result = await session.execute(select(UserExercise).where(UserExercise.muscle_id == selected_muscle))
    user_exercises = result.scalars().all()
    return base_exercises + user_exercises


