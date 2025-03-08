from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth_router, bookmarks_router, redirects_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(app)
    logger.info("Running some piece of code before start up.")
    yield
    logger.info("Running some piece of code after shut down.")

app = FastAPI(title="Bookmark URL Shortener API", lifespan=lifespan,
              description="This is a URL shortner application developed using FastAPI and Python.", version="V0")

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


@app.get("/", tags=["health"])
async def root():
    return {"message": "Welcome to the Bookmark URL Shortener API"}
