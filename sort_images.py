from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from shutil import copy2

def dms_to_decimal(dms,ref):
    degrees, minutes, seconds = dms
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

ip = None
geolocator = Nominatim(user_agent = "image_sorter")

for file in Path.cwd().iterdir():
    if file.suffix.lower() in IMAGE_EXTS:
        ip = file

        img = Image.open(ip)
        exif_data = img._getexif()
        if not exif_data:
            print("No exif data found")
            target_dir = Path("Sorted")/ "no_exif"
            target_dir.mkdir(parents=True, exist_ok=True)
            copy2(ip, target_dir / ip.name)
            continue
            
        gps_info = exif_data.get(34853)
        if not gps_info:
            print("no gps data found")
            target_dir = Path("Sorted")/ "no_gps"
            target_dir.mkdir(parents=True, exist_ok=True)
            copy2(ip, target_dir / ip.name)
            continue
    
        gps_readable = {}
        for key, value in gps_info.items():
            gps_readable[GPSTAGS.get(key,key)] = value
        required = ['GPSLatitude', 'GPSLatitudeRef', 'GPSLongitude', 'GPSLongitudeRef']
        if not all(k in gps_readable for k in required):
            print("Incomplete GPS data")
            target_dir = Path("Sorted")/ "no_gps"
            target_dir.mkdir(parents=True, exist_ok=True)
            copy2(ip, target_dir / ip.name)
            continue
        lat = dms_to_decimal(
            gps_readable['GPSLatitude'],
            gps_readable['GPSLatitudeRef']
         )
        lon = dms_to_decimal(
            gps_readable['GPSLongitude'],
            gps_readable['GPSLongitudeRef'],
            )
        location = geolocator.reverse((lat, lon), zoom = 10)
        if not location :
            target_dir = Path("Sorted")/ "Unknown_Location"
            target_dir.mkdir(parents=True, exist_ok=True)
            copy2(ip, target_dir / ip.name)
            continue
            
        address = location.raw.get("address", {})
        country = address.get("country") or "Unknown_country"
        state = address.get("state") or "Unknown_State"
        place = (address.get('city')\
                or address.get('town')\
                or address.get('state')\
                or "Unknown_Place"
                 )
        target_dir = Path("Sorted")/ country / state / place
        target_dir.mkdir(parents=True, exist_ok=True)
        
        copy2(ip, target_dir / ip.name)

