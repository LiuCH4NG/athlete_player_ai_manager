from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.database import engine, AsyncSessionLocal

from fastapi_mcp import FastApiMCP
from ai_assistant.mcp_app import create_agent, run_agent


# Create all tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@app.post(
    "/medical_supplies/",
    response_model=schemas.MedicalSupplyInDB,
    tags=["medical_supplies"],
    operation_id="create_medical_supply",
)
async def create_medical_supply(
    supply: schemas.MedicalSupplyCreate, db: AsyncSession = Depends(get_db)
):
    """
    创建新的医学耗材。

    在数据库中创建新耗材记录并返回创建的耗材信息。
    """
    return await crud.create_medical_supply(db=db, supply=supply)


@app.get(
    "/medical_supplies/",
    response_model=list[schemas.MedicalSupplyInDB],
    tags=["medical_supplies"],
    operation_id="list_medical_supplies",
)
async def read_medical_supplies(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    """
    获取医学耗材列表。

    支持分页获取耗材列表，可以指定跳过的记录数和每页的记录数限制。
    """
    supplies = await crud.get_medical_supplies(db, skip=skip, limit=limit)
    return supplies


@app.get(
    "/medical_supplies/{supply_id}",
    response_model=schemas.MedicalSupplyInDB,
    tags=["medical_supplies"],
    operation_id="get_medical_supply",
)
async def read_medical_supply(supply_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据ID获取特定医学耗材。

    通过耗材ID获取单个耗材的详细信息。
    """
    db_supply = await crud.get_medical_supply(db, supply_id=supply_id)
    if db_supply is None:
        raise HTTPException(status_code=404, detail="Medical supply not found")
    return db_supply


@app.put(
    "/medical_supplies/{supply_id}",
    response_model=schemas.MedicalSupplyInDB,
    tags=["medical_supplies"],
    operation_id="update_medical_supply",
)
async def update_medical_supply(
    supply_id: int, supply: schemas.MedicalSupplyUpdate, db: AsyncSession = Depends(get_db)
):
    """
    更新医学耗材信息。

    根据耗材ID更新指定耗材的信息。
    """
    db_supply = await crud.update_medical_supply(db, supply_id=supply_id, supply=supply)
    if db_supply is None:
        raise HTTPException(status_code=404, detail="Medical supply not found")
    return db_supply


@app.delete(
    "/medical_supplies/{supply_id}",
    response_model=schemas.MedicalSupplyInDB,
    tags=["medical_supplies"],
    operation_id="delete_medical_supply",
)
async def delete_medical_supply(supply_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除医学耗材。

    根据耗材ID删除指定的耗材记录。
    """
    db_supply = await crud.delete_medical_supply(db, supply_id=supply_id)
    if db_supply is None:
        raise HTTPException(status_code=404, detail="Medical supply not found")
    return db_supply


@app.post(
    "/medical_supplies/search/",
    response_model=list[schemas.MedicalSupplyInDB],
    tags=["medical_supplies"],
    operation_id="search_medical_supplies",
)
async def search_medical_supplies(
    search_params: schemas.MedicalSupplySearch,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    搜索医学耗材。

    根据一个或多个查询参数搜索耗材，支持在名称、编码、分类、规格、厂家、存储位置等字段中搜索。
    返回匹配的耗材列表，支持分页。
    """
    supplies = await crud.search_medical_supplies(
        db, search_params=search_params, skip=skip, limit=limit
    )
    return supplies


mcp = FastApiMCP(app)
mcp.mount_http()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")


@app.get("/chat/")
async def chat(message: str):
    agent = await create_agent()
    info = await run_agent(agent, message)
    return {"info": info}
