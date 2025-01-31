from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, model_validator, field_validator, Field
from pydantic_core.core_schema import ValidationInfo


class DatetimeRange(BaseModel):
    date_from: Optional[datetime] = Field(None)
    date_to: Optional[datetime] = Field(None)

    def are_both_dates_none(self):
        return self.date_from is None and self.date_to is None

    @model_validator(mode='after')
    def validate_date_range(self):
        if (self.date_from is None) != (self.date_to is None):
            raise ValueError('Both "Date From" and "Date To" must be either specified or not')

        if not self.are_both_dates_none() and (self.date_to < self.date_from):
            raise ValueError('"Date To" must be greater than "Date From"')

        return self