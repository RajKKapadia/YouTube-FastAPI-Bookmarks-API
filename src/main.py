from contextlib import asynccontextmanager
import logging
import sys
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth_router, bookmarks_router, redirects_router

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("bookmark-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting application: {app.title} v{app.version}")
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown initiated")


app = FastAPI(title="Bookmark URL Shortener API", lifespan=lifespan,
              description="This is a URL shortner application developed using FastAPI and Python.", version="V0")


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    return response

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
logger.info("Registering API routers")
app.include_router(auth_router)
app.include_router(bookmarks_router)
app.include_router(redirects_router)


@app.get("/", tags=["health"])
async def root():
    logger.debug("Health check endpoint called")
    return {"message": "Welcome to the Bookmark URL Shortener API"}
