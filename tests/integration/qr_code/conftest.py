from typing import List
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.models.user import User

from src.services.short_code_generator.implementation import ShortCodeGenerator


@pytest.fixture(scope='function')
async def prepopulated_urls(async_db: AsyncSession, user: User) -> List[ShortenedUrl]:
    short_code_generator = ShortCodeGenerator()

    twitch_url = ShortenedUrl(
        friendly_name="Twitch TV",
        is_short_code_custom=True,
        short_code="twitch-tv-url",
        long_url="https://www.twitch.tv/",
        user_id=user.id,
    )

    generate_short_code = short_code_generator.generate_short_code(code_length=8, max_retries=5)

    youtube_url = ShortenedUrl(
        friendly_name="Youtube",
        is_short_code_custom=False,
        short_code=next(generate_short_code),
        long_url="https://youtube.com/",
        user_id=user.id,
    )

    async_db.add(twitch_url)
    async_db.add(youtube_url)
    await async_db.commit()


    return [twitch_url, youtube_url]


@pytest.fixture(scope='function')
async def prepopulated_url_for_second_user(async_db: AsyncSession, second_user: User) -> ShortenedUrl:
    some_url = ShortenedUrl(
        friendly_name="Some wierd URL",
        is_short_code_custom=True,
        short_code="wierd-url",
        long_url="https://weirdo.com/",
        user_id=second_user.id,
    )

    async_db.add(some_url)
    await async_db.commit()

    return some_url


@pytest.fixture(scope='function')
async def prepopulated_qr_codes_for_first_user(
        async_db: AsyncSession, prepopulated_urls: List[ShortenedUrl], user: User,
) -> List[QRCode]:
    qr_code_to_twitch = QRCode(
        title="QR Code to the twitch.tv",
        image=None,
        customization={"hello": "world", "margin": 5},
        user_id=user.id,
        link_id=prepopulated_urls[0].id,
    )

    qr_code_to_youtube = QRCode(
        title="QR Code to the youtube.com",
        image=None,
        customization={"hello": "world", "margin": 5},
        user_id=user.id,
        link_id=prepopulated_urls[1].id,
    )

    async_db.add(qr_code_to_twitch)
    async_db.add(qr_code_to_youtube)

    await async_db.commit()
    return [qr_code_to_twitch, qr_code_to_youtube]


@pytest.fixture(scope='function')
async def prepopulated_qr_codes_for_second_user(
        async_db: AsyncSession, prepopulated_url_for_second_user: ShortenedUrl, second_user: User,
) -> List[QRCode]:
    qr_code_to_weird_url = QRCode(
        title="QR Code to the weird url",
        image=None,
        customization={"hello": "world", "margin": 5},
        user_id=second_user.id,
        link_id=prepopulated_url_for_second_user.id,
    )

    async_db.add(qr_code_to_weird_url)

    await async_db.commit()
    return [qr_code_to_weird_url]
