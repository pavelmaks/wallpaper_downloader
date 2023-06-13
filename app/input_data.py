import argparse
from validator import Validator
from now_date import NowDate


class InputData:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='Get input mounth and year')

    def parse_input_args(self) -> None:
        now_month, now_year = NowDate.get_default_date()
        self.parser.add_argument('-m', '--month', type=int, default=now_month)
        self.parser.add_argument('-y', '--year', type=int, default=now_year)
        self.parser.add_argument('-f', '--format', type=str, default='640x480')
        self.parse_args = self.parser.parse_args()

    def get_input_args(self) -> tuple[int, int, int]:
        self.parse_input_args()
        Validator(self.parse_args.month, self.parse_args.year, self.parse_args.format)
        return self.parse_args.month, self.parse_args.year, self.parse_args.format
