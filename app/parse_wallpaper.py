import os
import re
from calendar import month_name

import aiofiles
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from app.wallpaper_exception import (DownloadImageException,
                                     DownloadPageException)
from logs.logger import logger


class ParseWallpaper:
    def __init__(self, month: int, year: int, img_format: str) -> None:
        self.month = month
        self.year = year
        self.img_format = img_format
        self.base_url = 'https://www.smashingmagazine.com/'

    @property
    def download_directory(self) -> str:
        return f'images/{self.year}/{self.month_name_long}/{self.img_format}'

    @property
    def page_month_url(self) -> str:
        url = self.base_url
        url += f'{self.year if self.month > 1 else self.year - 1}/'
        url += f'{self.month - 1 if self.month > 1 else 12:02}'
        if self.year > 2013:
            url += f'/desktop-wallpaper-calendars-{self.month_name_long}-{self.year}/'
        else:
            url += f'/desktop-wallpaper-calendar-{self.month_name_long}-{self.year}/'
        return url

    @property
    def month_name_long(self) -> str:
        return month_name[self.month].lower()

    async def get_links_images(self) -> list[str] | None:
        async with self.session.get(self.page_month_url) as response:
            if response.status == 200:
                content = await response.read()
                soup = BeautifulSoup(content, 'html.parser')
                return [link.get('href') for link in soup.findAll('a', href=re.compile(f'{self.img_format}'))]
            elif response.status == 404:
                raise DownloadPageException(f'Страница не найдена: {self.page_month_url}')
            else:
                raise Exception('Другая ошибка')

    async def download_image(self, url: str) -> bytes | None:
        logger.info(f'download start {url.split("/")[-1]}')
        async with self.session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                logger.info(f'download end {url.split("/")[-1]}')
                return image_data
            elif response.status == 404:
                raise DownloadImageException(f'Изображение не найдено: {url}')
            else:
                raise Exception('Другая ошибка')

    async def process_image(self, image_data, filename):
        async with aiofiles.open(f'{self.download_directory}/{filename}', 'wb') as f:
            logger.info(f'wrile start {filename}')
            await f.write(image_data)
            logger.info(f'wrile end {filename}')

    async def download_and_write_images(self, links_images: list[str]) -> None:
        if not links_images:
            raise DownloadImageException(f'Изображение с форматом: {self.img_format} не найдены')
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)
        for link in links_images:
            try:
                bin_image = await self.download_image(link)
            except DownloadImageException as e:
                logger.error(str(e))
                break
            await self.process_image(bin_image, link.split("/")[-1])

    async def get_wallpaper(self) -> None:
        try:
            self.session = ClientSession(connector=aiohttp.TCPConnector(ssl=False))
            links_images = await self.get_links_images()
            await self.write_images(links_images)
        except DownloadPageException as page_error:
            logger.error(page_error)
        except Exception as error:
            logger.error(str(error))
        finally:
            await self.session.close()
