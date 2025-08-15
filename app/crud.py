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


async def search_athletes(db: AsyncSession, query: str, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Athlete)
        .filter(
            models.Athlete.is_deleted == False,
            or_(
                models.Athlete.name.ilike(f"%{query}%"),
                models.Athlete.sport_event.ilike(f"%{query}%"),
                models.Athlete.hometown.ilike(f"%{query}%"),
                models.Athlete.description.ilike(f"%{query}%"),
                models.Athlete.remarks.ilike(f"%{query}%"),
            ),
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
