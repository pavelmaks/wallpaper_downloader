import os
import re
from calendar import month_name

import aiohttp
import asyncio
from aiohttp import ClientSession
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Pool, cpu_count



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

    def get_links_images(self) -> list[str]:
        try:
            responce = requests.get(self.page_month_url)
            responce.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception('Page wallpaper error\n' + str(err))
        soup = BeautifulSoup(responce.content, 'html.parser')
        return [link.get('href') for link in soup.findAll('a', href=re.compile(f'{self.img_format}'))]

    # def write_images(self, images: list[str]) -> None:
    #     if not images:
    #         raise Exception('Walpapers not found')
    #     if not os.path.exists(self.download_directory):
    #         os.makedirs(self.download_directory)
    #     for image in images:
    #         with open(f'{self.download_directory}/{image.split("/")[-1]}', 'wb') as img:
    #             try:
    #                 p = requests.get(image)
    #                 p.raise_for_status()
    #             except requests.exceptions.HTTPError as err:
    #                 raise Exception('Image download error\n' + str(err))
    #             img.write(p.content)

    async def download_image(self, session: ClientSession, url: str) -> bytes | None:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                return image_data
            else:
                return None

    def process_image(self, image_data, filename):
        with open(f'{self.download_directory}/{filename}', 'wb') as f:
            f.write(image_data)
        print(f'Saved image: {filename}')

    def process_queue(self, queue):
        while True:
            item = queue.get()
            if item is None:
                break
            image_data, filename = item
            self.process_image(image_data, filename)
            queue.task_done()

    async def write_images(self, links_images: list[str]) -> None:
        self.queue = asyncio.Queue(maxsize=4)
        if not links_images:
            raise Exception('Walpapers not found')
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for link in links_images:
                bin_image = await self.download_image(session, link)
                await self.queue.put((bin_image, link.split("/")[-1]))
                await self.create_processes()
                # self.process_image(bin_image, link.split("/")[-1])

    async def create_processes(self):
        item = await self.queue.get()
        file_data, file_name = item
        p = Process(target=self.process_image, args=(file_data, file_name))
        p.start()

    def get_wallpaper(self):
        links_images = self.get_links_images()
        asyncio.run(self.write_images(links_images))
