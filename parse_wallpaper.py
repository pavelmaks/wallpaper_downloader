import os
import re
from calendar import month_name

import requests
from bs4 import BeautifulSoup


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
        return self.base_url +\
            f'{self.year}/{self.month - 1:02}/desktop-wallpaper-calendars-{self.month_name_long}-{self.year}/'

    @property
    def month_name_long(self) -> str:
        return month_name[self.month].lower()

    def get_links_images(self) -> list[str]:
        responce = requests.get(self.page_month_url)
        soup = BeautifulSoup(responce.content, 'html.parser')
        return [link.get('href') for link in soup.findAll('a', href=re.compile(f'{self.img_format}'))]

    def write_images(self, images: list[str]) -> None:
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)
        for image in images:
            with open(f'{self.download_directory}/{image.split("/")[-1]}', 'wb') as img:
                p = requests.get(image)
                img.write(p.content)

    def get_wallpaper(self):
        links_images = self.get_links_images()
        self.write_images(links_images)
