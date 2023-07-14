import re
from dataclasses import dataclass
from typing import ClassVar

from app.now_date import NowDate


@dataclass
class Validator:
    month: int
    year: int
    image_format: str
    COUNT_MONTH: ClassVar = 12

    def __post_init__(self):
        self.date_validator()
        self.format_validator()

    def date_validator(self) -> None:
        now_month, now_year = NowDate.get_default_date()
        if not 1 <= self.month <= self.COUNT_MONTH:
            raise ValueError('The month should be in the range from 1 to 12')
        if not 2010 <= self.year <= now_year:
            raise ValueError('The year should be in the range from 2010 to current year')
        if self.year == now_year and self.month > now_month:
            raise ValueError('The date cannot be later than the current date')

    def format_validator(self) -> None:
        match = re.fullmatch(r'\d+x\d+', self.image_format)
        if not match:
            raise ValueError('The format should be of the form (width)x(height), example: 640x480')
