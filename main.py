from app.input_data import InputData
from app.parse_wallpaper import ParseWallpaper


def main():
    input_data = InputData()
    month, year, img_format = input_data.get_input_args()
    parse_wallpaper = ParseWallpaper(month, year, img_format)
    parse_wallpaper.get_wallpaper()


if __name__ == '__main__':
    main()
