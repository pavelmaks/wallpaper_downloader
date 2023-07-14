import asyncio

import aiohttp
from aiohttp import ClientSession

from app.parse_wallpaper import ParseWallpaper
from logs.logger import logger

img_format = '640x480'
async def pages_test():
    for year in range(2017, 2024):
        for month in range(1, 13):
            print(f'{month} {year} {img_format}')
            obj = ParseWallpaper(month, year, img_format)
            obj.session = ClientSession(connector=aiohttp.TCPConnector(ssl=False))
            try:
                links = await obj.get_links_images()
            except Exception as e:
                logger.error(f'{month} {year} {img_format}', exc_info=True)
            else:
                logger.info(f'{month} {year} {img_format} DONE links:{len(links)}')
            finally:
                await obj.session.close()

asyncio.run(pages_test())
