from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pymysql
import logging

from src.database import engine, Base, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST
from src.routers import auth_router, bookmarks_router, redirects_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database if it doesn't exist


async def create_database():
    try:
        # Connect without specifying a database to create it
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Database '{DB_NAME}' created or verified")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise

# Create database tables


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database and tables on startup
    await create_database()
    await create_tables()
    yield

app = FastAPI(title="Bookmark URL Shortener API", lifespan=lifespan,
              description="This is a URL shortner application developed using FastAPI and Python.")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(bookmarks_router)
app.include_router(redirects_router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Bookmark URL Shortener API"}
