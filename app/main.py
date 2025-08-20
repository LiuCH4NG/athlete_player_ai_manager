from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware # 导入 CORS 中间件
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.database import engine, AsyncSessionLocal

from fastapi_mcp import FastApiMCP
from ai_assistant.mcp_app import create_agent, run_agent
import os # 导入 os 模块以读取环境变量


# Create all tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

# 配置 CORS
# 从环境变量读取允许的源，如果没有设置则默认为 ["*"] (允许所有源)
# 在生产环境中，强烈建议明确设置允许的源，例如 ["http://your-frontend-domain.com"]
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    origins = ["*"]
else:
    # 假设 ALLOWED_ORIGINS 是一个逗号分隔的字符串
    origins = [origin.strip() for origin in allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 允许所有方法 (GET, POST, etc.)
    allow_headers=["*"], # 允许所有头
    # expose_headers=["Access-Control-Allow-Origin"] # 如果需要暴露特定头给浏览器
)


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@app.post(
    "/athletes/",
    response_model=schemas.AthleteInDB,
    tags=["athletes"],
    operation_id="create_athlete",
)
async def create_athlete(
    athlete: schemas.AthleteCreate, db: AsyncSession = Depends(get_db)
):
    """
    创建新的运动员。

    在数据库中创建新运动员记录并返回创建的运动员信息。
    """
    return await crud.create_athlete(db=db, athlete=athlete)


@app.get(
    "/athletes/",
    response_model=list[schemas.AthleteInDB],
    tags=["athletes"],
    operation_id="list_athletes",
)
async def read_athletes(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    """
    获取运动员列表。

    支持分页获取运动员列表，可以指定跳过的记录数和每页的记录数限制。
    """
    athletes = await crud.get_athletes(db, skip=skip, limit=limit)
    return athletes


@app.get(
    "/athletes/{athlete_id}",
    response_model=schemas.AthleteInDB,
    tags=["athletes"],
    operation_id="get_athlete",
)
async def read_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据ID获取特定运动员。

    通过运动员ID获取单个运动员的详细信息。
    """
    db_athlete = await crud.get_athlete(db, athlete_id=athlete_id)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete


@app.put(
    "/athletes/{athlete_id}",
    response_model=schemas.AthleteInDB,
    tags=["athletes"],
    operation_id="update_athlete",
)
async def update_athlete(
    athlete_id: int, athlete: schemas.AthleteUpdate, db: AsyncSession = Depends(get_db)
):
    """
    更新运动员信息。

    根据运动员ID更新指定运动员的信息。
    """
    db_athlete = await crud.update_athlete(db, athlete_id=athlete_id, athlete=athlete)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete


@app.delete(
    "/athletes/{athlete_id}",
    response_model=schemas.AthleteInDB,
    tags=["athletes"],
    operation_id="delete_athlete",
)
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除运动员。

    根据运动员ID删除指定的运动员记录。
    """
    db_athlete = await crud.delete_athlete(db, athlete_id=athlete_id)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return db_athlete


@app.post(
    "/athletes/search/",
    response_model=list[schemas.AthleteInDB],
    tags=["athletes"],
    operation_id="search_athletes",
)
async def search_athletes(
    search_params: schemas.AthleteSearch,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    搜索运动员。

    根据一个或多个查询参数搜索运动员，支持在姓名、项目、籍贯、描述、备注等字段中搜索。
    返回匹配的运动员列表，支持分页。
    """
    athletes = await crud.search_athletes(
        db, search_params=search_params, skip=skip, limit=limit
    )
    return athletes


mcp = FastApiMCP(app)
mcp.mount_http()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

# 为 /favicon.ico 请求提供一个默认的空响应或重定向，以避免 404 错误
# 这里简单地返回一个空的 favicon.ico 文件响应，或者可以返回一个默认图标
# 为了简单起见，我们返回一个 204 No Content 响应
from fastapi.responses import Response
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204) # 返回 204 状态码表示无内容


@app.get("/chat/")
async def chat(message: str):
    agent = await create_agent()
    info = await run_agent(agent, message)
    return {"info": info}
