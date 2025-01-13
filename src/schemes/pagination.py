from pydantic import BaseModel, conint


class PaginationParams(BaseModel):
    page: conint(gt=0) = 1
    page_size: conint(gt=0) = 15 # Items per page


class PaginationResponse(BaseModel):
    current_page: int
    page_size: int
    total_pages: int
    total_items: int
