from abc import abstractmethod, ABC
from typing import Optional

from src.models.user import User
from src.repositories.base.abstract_sql import AbstractGenericRepository


class AbstractUserRepository(AbstractGenericRepository[User], ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()
