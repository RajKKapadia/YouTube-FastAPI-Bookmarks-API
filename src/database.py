import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src import config

logger = logging.getLogger("bookmark-api")

DB_USERNAME = config.DB_USERNAME
DB_PASSWORD = config.DB_PASSWORD
DB_HOST = config.DB_HOST
DB_NAME = config.DB_NAME
DB_PORT = config.DB_PORT

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
logger.info(
    f"Connecting to database: postgresql+asyncpg://{DB_USERNAME}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False  # Set to True to log all SQL queries (very verbose)
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def get_db():
    logger.debug("Creating new database session")
    try:
        async with AsyncSessionLocal() as session:
            yield session
            logger.debug("Database session closed")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
