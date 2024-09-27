from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config_data.config import DATABASE_URL

Base = declarative_base()

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

# Настройка асинхронной сессии
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# Инициализация базы данных (для создания таблиц)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
