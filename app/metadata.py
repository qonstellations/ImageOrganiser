from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_datetime(imgpath : str) -> datetime:
    image = Image.open(imgpath)

    exifdata = image.getexif()

    # DateTime TagID = 306

    datetime_str = exifdata[306]
    # DateTime format example = str(2025:09:07 06:46:22)

    datetime_str = datetime_str.replace(":", "-", 2).replace(" ", "T", 1)

    datetime_obj = datetime.fromisoformat(datetime_str)

    return datetime_obj

def get_gps(imgpath : str):
    # GPSInfo TagID = 34853
    pass