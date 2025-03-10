from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.database import get_db
from src.models.bookmark import Bookmark
from src.models.user import User
from src.schemas.bookmark import BookmarkCreate, BookmarkResponse
from src.utils.auth import get_current_active_user
from src.utils.shortener import create_unique_short_code

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@router.post("/create", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    bookmark: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    short_code = await create_unique_short_code(db)

    db_bookmark = Bookmark(
        original_url=str(bookmark.original_url),
        short_code=short_code,
        user_id=current_user.id
    )

    db.add(db_bookmark)
    await db.commit()
    await db.refresh(db_bookmark)

    return db_bookmark


@router.get("/get/all", response_model=List[BookmarkResponse])
async def get_user_bookmarks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Bookmark).filter(Bookmark.user_id == current_user.id)
    )
    bookmarks = result.scalars().all()
    return bookmarks


@router.get("/get/{bookmark_id}", response_model=BookmarkResponse)
async def get_bookmark(
    bookmark_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Bookmark).filter(
            Bookmark.id == bookmark_id,
            Bookmark.user_id == current_user.id
        )
    )
    bookmark = result.scalars().first()

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    return bookmark


@router.delete("/delete/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookmark(
    bookmark_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Bookmark).filter(
            Bookmark.id == bookmark_id,
            Bookmark.user_id == current_user.id
        )
    )
    bookmark = result.scalars().first()

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    await db.delete(bookmark)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
