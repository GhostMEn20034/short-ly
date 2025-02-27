from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.repositories.base.implementation import GenericRepositoryImplementation
from src.repositories.qr_code.abstract import AbstractQRCodeRepository


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
        qr_code, shortened_url = result.first()
        qr_code.link = shortened_url
        return qr_code
