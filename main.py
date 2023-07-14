import asyncio
from time import time

from app.input_data import InputData
from app.parse_wallpaper import ParseWallpaper
from logs.logger import logger


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logger.info(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func

@timer_func
def main():
    input_data = InputData()
    month, year, img_format = input_data.get_input_args()
    parse_wallpaper = ParseWallpaper(month, year, img_format)
    asyncio.run(parse_wallpaper.get_wallpaper())


if __name__ == '__main__':
    main()
