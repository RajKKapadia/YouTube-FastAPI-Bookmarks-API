from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_db
from src.models.bookmark import Bookmark

router = APIRouter(tags=["redirects"])


@router.get("/{short_code}")
async def redirect_to_url(short_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bookmark).filter(Bookmark.short_code == short_code))
    bookmark = result.scalars().first()

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    # Increment visit count
    bookmark.visit_count += 1
    await db.commit()

    return RedirectResponse(url=bookmark.original_url)
