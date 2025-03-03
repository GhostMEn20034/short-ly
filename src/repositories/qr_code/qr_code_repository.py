from typing import Optional, Sequence, Tuple
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func

from src.models.user import User
from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.repositories.base.implementation import GenericRepositoryImplementation
from src.repositories.qr_code.abstract import AbstractQRCodeRepository
from src.schemes.pagination import PaginationParams


class QRCodeRepository(GenericRepositoryImplementation[QRCode], AbstractQRCodeRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, QRCode)

    async def get_by_link_id(self, link_id: int) -> Optional[QRCode]:
        stmt = select(QRCode).where(QRCode.link_id == link_id)
        result = await self._session.exec(stmt)
        return result.first()

    async def get_by_id_with_joined_link(self, qr_code_id: int) -> Optional[QRCode]:
        stmt = select(QRCode, ShortenedUrl).where(QRCode.id == qr_code_id).join(ShortenedUrl)
        result = await self._session.exec(stmt)
        row = result.first()
        if row is None:
            return None

        qr_code, shortened_url = row
        qr_code.link = shortened_url
        return qr_code

    async def get_paginated_list_of_qr_codes_with_joined_links(
            self, user: User, pagination_params: PaginationParams) -> Tuple[Sequence[QRCode], int]:
        offset, limit = pagination_params.get_offset_and_limit()

        stmt = (
            select(
                QRCode,
                ShortenedUrl,
                func.count().over().label("total_count"),
            )
            .where(QRCode.user_id == user.id)
            .join(ShortenedUrl)
        )
        # ORDER BY → OFFSET → LIMIT
        stmt = (
            stmt
            .order_by(desc(QRCode.created_at))
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.exec(stmt)
        rows = result.all()

        if rows:
            paginated_items = [
                QRCode(
                    **row[0].model_dump(),
                    link=row[1]  # Attach the ShortenedUrl object to the QRCode
                )
                for row in rows
            ]
            total_count = rows[0][2]  # Extract total_count from the first row
        else:
            paginated_items = []
            total_count = 0

        return paginated_items, total_count
