from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config_data.config import Config, load_config
from .models import Base
import logging

config: Config = load_config()
POSTGRES_DSN: str = config.tg_bot.postgres_dsn

logger = logging.getLogger(__name__)

engine = create_async_engine(POSTGRES_DSN, echo=False)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db():
    async with engine.begin() as conn:
        logger.info('Creating all tables')
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info('Tables created')
        except Exception as e:
            logger.error(f"Error occurred: {e}")
