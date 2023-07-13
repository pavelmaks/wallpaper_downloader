from app.parse_wallpaper import ParseWallpaper
from logs.logger import logger


img_format = '640x480'
for year in range(2011, 2023):
    for month in range(1, 13):
        print(f'{month} {year} {img_format}')
        obj = ParseWallpaper(month, year, img_format)
        try:
            links = obj.get_links_images()
        except Exception as e:
            logger.error(f'{month} {year} {img_format}', exc_info=True)
        else:
            logger.info(f'{month} {year} {img_format} DONE links:{len(links)}')
