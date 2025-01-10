from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import ShortenedUrl
from src.repositories.base.implementation_sql import GenericRepositoryImplementation
from .abstract_sql import AbstractURLRepositorySQL


class URLRepositorySQL(GenericRepositoryImplementation[ShortenedUrl], AbstractURLRepositorySQL):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ShortenedUrl)

    async def get_by_short_code(self, short_code: str) -> Optional[ShortenedUrl]:
        stmt = select(ShortenedUrl).where(ShortenedUrl.short_code == short_code)
        result = await self._session.exec(stmt)
        return result.first()

    async def is_shortened_url_exist(self, short_code: str) -> bool:
        stmt = select(ShortenedUrl).where(ShortenedUrl.short_code == short_code)
        result = await self._session.exec(stmt)
        return bool(result.first())
