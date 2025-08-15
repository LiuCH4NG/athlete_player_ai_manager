from fastapi import FastAPI, Depends, HTTPException, status
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

@app.post("/athletes/", response_model=schemas.AthleteInDB, tags=["athletes"], operation_id="create_athlete")
async def create_athlete(athlete: schemas.AthleteCreate, db: AsyncSession = Depends(get_db)):
    """
    创建新的运动员。
    
    在数据库中创建新运动员记录并返回创建的运动员信息。
    """
    return await crud.create_athlete(db=db, athlete=athlete)

@app.get("/athletes/", response_model=list[schemas.AthleteInDB], tags=["athletes"], operation_id="list_athletes")
async def read_athletes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    获取运动员列表。
    
    支持分页获取运动员列表，可以指定跳过的记录数和每页的记录数限制。
    """
    athletes = await crud.get_athletes(db, skip=skip, limit=limit)
    return athletes

@app.get("/athletes/{athlete_id}", response_model=schemas.AthleteInDB, tags=["athletes"], operation_id="get_athlete")
async def read_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据ID获取特定运动员。
    
    通过运动员ID获取单个运动员的详细信息。
    """
    db_athlete = await crud.get_athlete(db, athlete_id=athlete_id)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete

@app.put("/athletes/{athlete_id}", response_model=schemas.AthleteInDB, tags=["athletes"], operation_id="update_athlete")
async def update_athlete(athlete_id: int, athlete: schemas.AthleteUpdate, db: AsyncSession = Depends(get_db)):
    """
    更新运动员信息。
    
    根据运动员ID更新指定运动员的信息。
    """
    db_athlete = await crud.update_athlete(db, athlete_id=athlete_id, athlete=athlete)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete

@app.delete("/athletes/{athlete_id}", response_model=schemas.AthleteInDB, tags=["athletes"], operation_id="delete_athlete")
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除运动员。
    
    根据运动员ID删除指定的运动员记录。
    """
    db_athlete = await crud.delete_athlete(db, athlete_id=athlete_id)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete

@app.get("/athletes/search/", response_model=list[schemas.AthleteInDB], tags=["athletes"], operation_id="search_athletes")
async def search_athletes(query: str, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    搜索运动员。
    
    根据关键词搜索运动员，支持在姓名、项目、籍贯、描述、备注等字段中搜索。
    返回匹配的运动员列表，支持分页。
    """
    athletes = await crud.search_athletes(db, query=query, skip=skip, limit=limit)
    return athletes

mcp = FastApiMCP(app)
mcp.mount_http()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

@app.get("/chat/")
async def chat(message: str):
    agent = await create_agent()
    info = await run_agent(agent, message)
    return {
        "info": info
    }