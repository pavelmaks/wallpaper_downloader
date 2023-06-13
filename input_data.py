import argparse
from datetime import datetime


class InputData:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='Get input mounth and year')

    @staticmethod
    def get_default_date() -> tuple[int, int]:
        """Метод получения текущего месяца и года"""
        date = datetime.now()
        return date.month, date.year

    def date_validator():
        pass

    def format_validator():
        pass

    def get_input_args(self) -> tuple[int, int, int]:
        now_month, now_year = self.get_default_date()
        self.parser.add_argument('-m', '--month', type=int, default=now_month)
        self.parser.add_argument('-y', '--year', type=int, default=now_year)
        self.parser.add_argument('-f', '--format', type=str, default='640x480')
        parse_args = self.parser.parse_args()
        return parse_args.month, parse_args.year, parse_args.format
