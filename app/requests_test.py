from input_data import InputData
from parse_wallpaper import ParseWallpaper

with open('log.txt', 'w') as f:
    f.seek(0)
    img_format = '640x480'
    for year in range(2010, 2023):
        for month in range(1, 13):
            print(f'{month} {year} {img_format}')
            obj = ParseWallpaper(month, year, img_format)
            try:
                links = obj.get_links_images()
            except Exception as e:
                f.write(f'{month} {year} {img_format} ERROR\n {e} \n')
            else:
                f.write(f'{month} {year} {img_format} DONE links:{len(links)}\n')
