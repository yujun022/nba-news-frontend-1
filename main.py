ffrom fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv  # 引入 dotenv 模組

# 載入 .env 文件中的環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 讀取環境變數中的 DATABASE_URL
#mysql+pymysql://<username>:<password>@nba_mysql:3306/<database_name>
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@nba_mysql:3306/nba_news")

# 設置非同步資料庫引擎
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

# 定義資料表
class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False, unique=True)

# FastAPI 應用
app = FastAPI()

# 設定 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可根據需求修改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 取得非同步資料庫 Session
async def get_db():
    async with SessionLocal() as session:
        yield session

# 創建資料表
@app.on_event("startup")
async def startup():
    # 建立資料表
    async with engine.begin() as conn:
        # 自動創建資料表
        await conn.run_sync(Base.metadata.create_all)

# 新增 API 端點
@app.get("/news")
async def get_news(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM news")
    return result.mappings().all()

@app.get("/news/{news_id}")
async def get_news_detail(news_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(f"SELECT * FROM news WHERE id = {news_id}")
    news_item = result.mappings().first()
    if news_item is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news_item

class NewsCreate(BaseModel):
    title: str
    link: str

@app.post("/news")
async def create_news(news: NewsCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(f"SELECT * FROM news WHERE link = '{news.link}'")
    existing_news = result.mappings().first()
    if existing_news:
        raise HTTPException(status_code=400, detail="News already exists")
    
    new_news = News(title=news.title, link=news.link)
    db.add(new_news)
    await db.commit()
    await db.refresh(new_news)
    return new_news
