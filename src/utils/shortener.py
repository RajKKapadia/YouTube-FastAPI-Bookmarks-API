import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.bookmark import Bookmark

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

async def create_unique_short_code(db: AsyncSession):
    while True:
        short_code = generate_short_code()
        result = await db.execute(select(Bookmark).filter(Bookmark.short_code == short_code))
        exists = result.scalars().first()
        if not exists:
            return short_code