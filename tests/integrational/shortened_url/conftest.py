from typing import List
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.shortened_url import ShortenedUrl
from src.models.shortened_url import User

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
