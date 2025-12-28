from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime

def get_datetime(imgpath : str) -> datetime:
    image = Image.open(imgpath)
    exifdata = image.getexif()

    # DateTime TagID = 306
    datetime_str = exifdata[306]

    # DateTime format example = str(2025:09:07 06:46:22)
    # this line converts the string to a format readable for datetime.fromisoformat method
    datetime_str = datetime_str.replace(":", "-", 2).replace(" ", "T", 1)
    datetime_obj = datetime.fromisoformat(datetime_str)

    return datetime_obj

def get_gps(imgpath : str) -> tuple:
    image = Image.open(imgpath)
    exifdata = image.getexif()
    
    # GPSInfo TagID = 34853
    gps_info = exifdata.get_ifd(34853)
    gps_data = {}

    if gps_info:
        for key, val in gps_info.items():
            decoded = GPSTAGS.get(key, key)
            gps_data[decoded] = val
    else:
        raise ValueError("No GPS data!")
    
    # {'GPSLatitudeRef': 'N', 
    # 'GPSLatitude': (18.0, 30.0, 42.07), 
    # 'GPSLongitudeRef': 'E', 
    # 'GPSLongitude': (73.0, 56.0, 30.81)}
    # GPS data format example

    # Converting Degree-Minute-Second to Decimal Degree 
    # & applying appropriate sign convention
    lat = gps_data["GPSLatitude"][0] + (gps_data["GPSLatitude"][1])/60 + (gps_data["GPSLatitude"][2])/3600
    lat = lat if gps_data["GPSLatitudeRef"] == "N" else -lat

    lon = gps_data["GPSLongitude"][0] + (gps_data["GPSLongitude"][1])/60 + (gps_data["GPSLongitude"][2])/3600
    lon = lon if gps_data["GPSLongitudeRef"] == "E" else -lon

    return (round(float(lat), 3), round(float(lon), 3))