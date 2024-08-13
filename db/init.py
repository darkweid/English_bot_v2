from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base
import logging

logger = logging.getLogger(__name__)
# DATABASE_URL = "sqlite+aiosqlite:///./english_bot.db"
DATABASE_URL = "postgresql+asyncpg://superuser:superpassword@postgres:5432/data"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db():
    async with engine.begin() as conn:
        logger.info('Creating all tables')
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info('Tables created')
        except Exception as e:
            logger.error(f"Error occurred: {e}")
