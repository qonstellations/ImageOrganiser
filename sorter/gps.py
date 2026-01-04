from pathlib import Path
from PIL import Image
from PIL.ExifTags import GPSTAGS
from geopy.geocoders import Nominatim
from shutil import copy2

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def dms_to_decimal(dms, ref):
    degrees, minutes, seconds = dms
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ("S", "W"):
        decimal = -decimal
    return decimal

def gps_sort(input_dir: Path, output_dir: Path | None = None):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir) if output_dir else input_dir / "GPS_Sorted"

    geolocator = Nominatim(user_agent="gps_sort")

    for file in input_dir.iterdir():
        if file.suffix.lower() not in IMAGE_EXTS:
            continue

        try:
            img = Image.open(file)
            exif = img._getexif()
        except Exception:
            target = output_dir / "no_exif"
            target.mkdir(parents=True, exist_ok=True)
            copy2(file, target / file.name)
            continue

        if not exif:
            target = output_dir / "no_exif"
            target.mkdir(parents=True, exist_ok=True)
            copy2(file, target / file.name)
            continue

        gps_info = exif.get(34853)
        if not gps_info:
            target = output_dir / "no_gps"
            target.mkdir(parents=True, exist_ok=True)
            copy2(file, target / file.name)
            continue

        gps_readable = {
            GPSTAGS.get(k, k): v for k, v in gps_info.items()
        }

        required = {
            "GPSLatitude",
            "GPSLatitudeRef",
            "GPSLongitude",
            "GPSLongitudeRef",
        }

        if not required.issubset(gps_readable):
            target = output_dir / "no_gps"
            target.mkdir(parents=True, exist_ok=True)
            copy2(file, target / file.name)
            continue

        lat = dms_to_decimal(
            gps_readable["GPSLatitude"],
            gps_readable["GPSLatitudeRef"],
        )
        lon = dms_to_decimal(
            gps_readable["GPSLongitude"],
            gps_readable["GPSLongitudeRef"],
        )

        location = geolocator.reverse((lat, lon), zoom=10)
        if not location:
            target = output_dir / "Unknown_Location"
            target.mkdir(parents=True, exist_ok=True)
            copy2(file, target / file.name)
            continue

        address = location.raw.get("address", {})
        country = address.get("country", "Unknown_Country")
        state = address.get("state", "Unknown_State")
        place = (
            address.get("city")
            or address.get("town")
            or address.get("state")
            or "Unknown_Place"
        )

        target = output_dir / country / state / place
        target.mkdir(parents=True, exist_ok=True)
        copy2(file, target / file.name)
