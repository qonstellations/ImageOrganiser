from PIL import Image
from datetime import datetime, timedelta
from pathlib import Path
from shutil import copy2
from sorter import IMAGE_EXTS

MOMENT_GAP = timedelta(minutes=30)

def get_datetime(imgpath: Path) -> datetime:
    try:
        image = Image.open(str(imgpath))
        exifdata = image.getexif()

        # DateTime TagID = 306
        datetime_str = exifdata[306]

        # DateTime format example = str(2025:09:07 06:46:22)
        # this line converts the string to a format readable for datetime.fromisoformat method
        datetime_str = datetime_str.replace(":", "-", 2).replace(" ", "T", 1)
        datetime_obj = datetime.fromisoformat(datetime_str)

        return datetime_obj
    except Exception:
        return None
    
def time_sort(input_dir: Path, output_dir: Path | None = None):
    input_dir = Path(input_dir)
    
    # Fetching all photos in directory
    photos = []
    for entry in input_dir.iterdir():
        if entry.is_file() and (entry.suffix.lower() in IMAGE_EXTS):
            dt = get_datetime(entry)
            if dt:
                photos.append((entry, dt))

    # Ignoring folders with no moments
    if len(photos) < 2:
        return

    # Sorting photos according to datetime objects
    photos.sort(key=lambda x: x[1])
    moments = []
    curr_moment = [photos[0]]

    # Calculating and appending individual moments
    for prev_photo, curr_photo in zip(photos, photos[1:]):
        if curr_photo[1] - prev_photo[1] <= MOMENT_GAP:
            curr_moment.append(curr_photo)
        else:
            moments.append(curr_moment)
            curr_moment = [curr_photo]
    moments.append(curr_moment)

    # Creating the moments
    for moment in moments:
        if len(moment) < 2:
            continue
        else:
            moment_time = moment[0][1].strftime("%Y-%m-%d_%H:%M:%S")
            folder = input_dir / Path(f"Moment_{moment_time}")
            folder.mkdir(parents=True, exist_ok=True)

            for photo, _ in moment:
                copy2(photo, folder / photo.name)
