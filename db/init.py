from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./english_bot.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db():
    async with engine.begin() as conn:
        logger.info('Creating all tables')
        await conn.run_sync(Base.metadata.create_all)
        logger.info('Tables created')
