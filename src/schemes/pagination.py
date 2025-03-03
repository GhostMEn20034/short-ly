import math
from typing import Tuple
from pydantic import BaseModel, conint


class PaginationParams(BaseModel):
    page: conint(gt=0) = 1
    page_size: conint(gt=0) = 15 # Items per page

    def get_offset_and_limit(self) -> Tuple[int, int]:
        """
        :return: Offset (first tuple value), limit (the second one)
        """
        offset = (self.page - 1) * self.page_size
        limit = self.page_size

        return offset, limit

    def get_total_pages(self, total_count: int):
        """
        :param total_count: Total number of items returned
        """
        total_pages = math.ceil(total_count / self.page_size)
        # By default, pagination should always result
        # in at least one "page" (even if it's empty), so this block of code ensures that total_pages is at least 1.
        if total_pages < 1:
            total_pages = 1

        return total_pages


class PaginationResponse(BaseModel):
    current_page: int
    page_size: int
    total_pages: int
    total_items: int

    class Config:
        json_schema_extra = {
            "example": {
                "current_page": 1,
                "page_size": 15,
                "total_pages": 1,
                "total_items": 1,
            }
        }
