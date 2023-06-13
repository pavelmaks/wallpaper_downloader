from datetime import datetime


class NowDate:
    @staticmethod
    def get_default_date() -> tuple[int, int]:
        """Метод получения текущего месяца и года"""
        date = datetime.now()
        return date.month, date.year
