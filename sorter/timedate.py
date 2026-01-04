from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
from pathlib import Path

def get_datetime(imgpath : Path) -> datetime:
    image = Image.open(str(imgpath))
    exifdata = image.getexif()

    # DateTime TagID = 306
    datetime_str = exifdata[306]

    # DateTime format example = str(2025:09:07 06:46:22)
    # this line converts the string to a format readable for datetime.fromisoformat method
    datetime_str = datetime_str.replace(":", "-", 2).replace(" ", "T", 1)
    datetime_obj = datetime.fromisoformat(datetime_str)

    return datetime_obj
    
def sort_by_time(dirpath : Path, day : bool = False, month : bool = False, year : bool = False):
    entries = dict()
    
    for entry in dirpath.iterdir():
        if entry.is_file() and entry.name.endswith(".jpg"):
            dt_data = get_datetime(entry)
            entries[f"{entry}"] = dt_data

    # entries dict is initialised with data now

    if year:
        dt_list = sorted(set(list(entries.values())))
        print(dt_list)
        for dt in dt_list:
            try:
                fpath = Path(f"images/{dt.year}")
                fpath.mkdir(parents=True, exist_ok=True)
                print(f"Directory '{fpath}' ensured to exist.")
            except OSError as e:
                print(f"Error creating directory: {e}")