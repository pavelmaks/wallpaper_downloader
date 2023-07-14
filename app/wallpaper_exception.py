class ExceptionWallpaper(Exception):
    """Общий класс исключения при работе с Wallpaper"""
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"Ошибка: {self.message}"


class DownloadPageException(ExceptionWallpaper):
    """Класс исключения при загрузке страницы с обоями"""

class DownloadImageException(ExceptionWallpaper):
    """Класс исключения при загрузке картинки"""
