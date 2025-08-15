from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app import models, schemas


async def get_athlete(db: AsyncSession, athlete_id: int):
    result = await db.execute(
        select(models.Athlete).filter(
            models.Athlete.id == athlete_id, 
            models.Athlete.is_deleted == False
        )
    )
    return result.scalars().first()


async def get_athletes(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Athlete)
        .filter(models.Athlete.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_athlete(db: AsyncSession, athlete: schemas.AthleteCreate):
    db_athlete = models.Athlete(**athlete.model_dump())
    db.add(db_athlete)
    await db.commit()
    await db.refresh(db_athlete)
    return db_athlete


async def update_athlete(
    db: AsyncSession, athlete_id: int, athlete: schemas.AthleteUpdate
):
    result = await db.execute(
        select(models.Athlete).filter(
            models.Athlete.id == athlete_id, models.Athlete.is_deleted == False
        )
    )
    db_athlete = result.scalars().first()
    if db_athlete:
        update_data = athlete.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_athlete, key, value)
        await db.commit()
        await db.refresh(db_athlete)
    return db_athlete


async def delete_athlete(db: AsyncSession, athlete_id: int):
    result = await db.execute(
        select(models.Athlete).filter(
            models.Athlete.id == athlete_id, models.Athlete.is_deleted == False
        )
    )
    db_athlete = result.scalars().first()
    if db_athlete:
        db_athlete.is_deleted = True
        await db.commit()
        await db.refresh(db_athlete)
    return db_athlete


async def search_athletes(
    db: AsyncSession, search_params: schemas.AthleteSearch, skip: int = 0, limit: int = 10
):
    query = select(models.Athlete).filter(models.Athlete.is_deleted == False)

    if search_params.name:
        query = query.filter(models.Athlete.name.ilike(f"%{search_params.name}%"))
    if search_params.sport_event:
        query = query.filter(
            models.Athlete.sport_event.ilike(f"%{search_params.sport_event}%")
        )
    if search_params.hometown:
        query = query.filter(
            models.Athlete.hometown.ilike(f"%{search_params.hometown}%")
        )
    if search_params.description:
        query = query.filter(
            models.Athlete.description.ilike(f"%{search_params.description}%")
        )
    if search_params.remarks:
        query = query.filter(models.Athlete.remarks.ilike(f"%{search_params.remarks}%"))
    if search_params.min_age:
        query = query.filter(models.Athlete.age >= search_params.min_age)
    if search_params.max_age:
        query = query.filter(models.Athlete.age <= search_params.max_age)
    if search_params.min_height:
        query = query.filter(models.Athlete.height >= search_params.min_height)
    if search_params.max_height:
        query = query.filter(models.Athlete.height <= search_params.max_height)
    if search_params.min_weight:
        query = query.filter(models.Athlete.weight >= search_params.min_weight)
    if search_params.max_weight:
        query = query.filter(models.Athlete.weight <= search_params.max_weight)

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()
