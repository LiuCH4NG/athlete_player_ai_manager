from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app import models, schemas


async def get_medical_supply(db: AsyncSession, supply_id: int):
    result = await db.execute(
        select(models.MedicalSupply).filter(
            models.MedicalSupply.id == supply_id,
            models.MedicalSupply.is_deleted == False
        )
    )
    return result.scalars().first()


async def get_medical_supplies(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.MedicalSupply)
        .filter(models.MedicalSupply.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_medical_supply(db: AsyncSession, supply: schemas.MedicalSupplyCreate):
    db_supply = models.MedicalSupply(**supply.model_dump())
    db.add(db_supply)
    await db.commit()
    await db.refresh(db_supply)
    return db_supply


async def update_medical_supply(
    db: AsyncSession, supply_id: int, supply: schemas.MedicalSupplyUpdate
):
    result = await db.execute(
        select(models.MedicalSupply).filter(
            models.MedicalSupply.id == supply_id, models.MedicalSupply.is_deleted == False
        )
    )
    db_supply = result.scalars().first()
    if db_supply:
        update_data = supply.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_supply, key, value)
        await db.commit()
        await db.refresh(db_supply)
    return db_supply


async def delete_medical_supply(db: AsyncSession, supply_id: int):
    result = await db.execute(
        select(models.MedicalSupply).filter(
            models.MedicalSupply.id == supply_id, models.MedicalSupply.is_deleted == False
        )
    )
    db_supply = result.scalars().first()
    if db_supply:
        db_supply.is_deleted = True
        await db.commit()
        await db.refresh(db_supply)
    return db_supply


async def search_medical_supplies(
    db: AsyncSession, search_params: schemas.MedicalSupplySearch, skip: int = 0, limit: int = 10
):
    query = select(models.MedicalSupply).filter(models.MedicalSupply.is_deleted == False)

    if search_params.name:
        query = query.filter(models.MedicalSupply.name.ilike(f"%{search_params.name}%"))
    if search_params.code:
        query = query.filter(models.MedicalSupply.code.ilike(f"%{search_params.code}%"))
    if search_params.category:
        query = query.filter(models.MedicalSupply.category.ilike(f"%{search_params.category}%"))
    if search_params.specification:
        query = query.filter(models.MedicalSupply.specification.ilike(f"%{search_params.specification}%"))
    if search_params.manufacturer:
        query = query.filter(models.MedicalSupply.manufacturer.ilike(f"%{search_params.manufacturer}%"))
    if search_params.storage_location:
        query = query.filter(models.MedicalSupply.storage_location.ilike(f"%{search_params.storage_location}%"))
    if search_params.description:
        query = query.filter(models.MedicalSupply.description.ilike(f"%{search_params.description}%"))
    if search_params.remarks:
        query = query.filter(models.MedicalSupply.remarks.ilike(f"%{search_params.remarks}%"))
    if search_params.batch_number:
        query = query.filter(models.MedicalSupply.batch_number.ilike(f"%{search_params.batch_number}%"))
    if search_params.min_price:
        query = query.filter(models.MedicalSupply.unit_price >= search_params.min_price)
    if search_params.max_price:
        query = query.filter(models.MedicalSupply.unit_price <= search_params.max_price)
    if search_params.min_stock:
        query = query.filter(models.MedicalSupply.stock_quantity >= search_params.min_stock)
    if search_params.max_stock:
        query = query.filter(models.MedicalSupply.stock_quantity <= search_params.max_stock)
    if search_params.expiry_date:
        query = query.filter(models.MedicalSupply.expiry_date <= search_params.expiry_date)

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()
