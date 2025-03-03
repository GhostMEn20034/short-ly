from typing import Optional, Sequence, Tuple

from sqlalchemy import func
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.shortened_url import ShortenedUrl
from src.models.qr_code import QRCode
from src.repositories.base.implementation import GenericRepositoryImplementation
from .abstract import AbstractURLRepositorySQL
from src.schemes.pagination import PaginationParams
from src.schemes.common import DatetimeRange


class URLRepositorySQL(GenericRepositoryImplementation[ShortenedUrl], AbstractURLRepositorySQL):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ShortenedUrl)

    async def get_by_short_code(self, short_code: str) -> Optional[ShortenedUrl]:
        stmt = select(ShortenedUrl).where(ShortenedUrl.short_code == short_code)
        result = await self._session.exec(stmt)
        return result.first()

    async def get_by_short_code_with_joined_qr_code(self, short_code: str) -> Tuple[
        Optional[ShortenedUrl], Optional[QRCode]
    ]:
        stmt = select(ShortenedUrl, QRCode).where(ShortenedUrl.short_code == short_code).outerjoin(QRCode)
        result = await self._session.exec(stmt)
        row = result.first()
        if row is None:
            return None, None

        shortened_url, qr_code = row
        return shortened_url, qr_code

    async def get_paginated_url_list(self, user_id: int, datetime_range: DatetimeRange,
                                     pagination_params: PaginationParams) -> Tuple[Sequence[ShortenedUrl], int]:
        offset, limit = pagination_params.get_offset_and_limit()

        stmt = (
            select(
                ShortenedUrl,
                func.count().over().label("total_count"),
            )
            .where(ShortenedUrl.user_id == user_id)
        )
        if not datetime_range.are_both_dates_none():
            stmt = stmt.where(
                ShortenedUrl.created_at >= datetime_range.date_from,
                ShortenedUrl.created_at <= datetime_range.date_to,
            )

        # ORDER BY → OFFSET → LIMIT
        stmt = (
            stmt
            .order_by(desc(ShortenedUrl.created_at))
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.exec(stmt)
        rows = result.all()

        if rows:
            paginated_items = [row[0] for row in rows]  # Extract ShortenedUrl objects
            total_count = rows[0][1]  # Extract total_count from the first row
        else:
            paginated_items = []
            total_count = 0

        return paginated_items, total_count

    async def get_paginated_url_list_with_qr(
            self, user_id: int, datetime_range: DatetimeRange, pagination_params: PaginationParams
    ) -> Tuple[Sequence[Tuple[ShortenedUrl, Optional[int]]], int]:
        offset, limit = pagination_params.get_offset_and_limit()

        stmt = (
            select(
                ShortenedUrl,
                QRCode.id,  # Select QR Code ID
                func.count().over().label("total_count"),
            )
            .outerjoin(QRCode)
            .where(ShortenedUrl.user_id == user_id)
        )

        if not datetime_range.are_both_dates_none():
            stmt = stmt.where(
                ShortenedUrl.created_at >= datetime_range.date_from,
                ShortenedUrl.created_at <= datetime_range.date_to,
            )

        stmt = stmt.order_by(desc(ShortenedUrl.created_at)).offset(offset).limit(limit)

        result = await self._session.exec(stmt)
        rows = result.all()

        if rows:
            paginated_items = [(row[0], row[1]) for row in rows]  # Extract ShortenedUrl and optional QRCode ID
            total_count = rows[0][2]  # Extract total_count from the first row
        else:
            paginated_items = []
            total_count = 0

        return paginated_items, total_count

    async def is_shortened_url_exist(self, short_code: str) -> bool:
        stmt = select(ShortenedUrl).where(ShortenedUrl.short_code == short_code)
        result = await self._session.exec(stmt)
        return bool(result.first())
