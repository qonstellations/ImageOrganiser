from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

from sorter.gps import gps_sort
from sorter.time import time_sort

def contains_images(folder: Path) -> bool:
    return any(
        p.is_file() and p.suffix.lower() in IMAGE_EXTS
        for p in folder.iterdir()
    )

def master_sort(input_dir: Path):
    input_dir = Path(input_dir)

    print("Initialising sorting...")

    gps_sort(input_dir, output_dir=input_dir / "Sorted")
    working_dir = input_dir / "Sorted"

    for folder in working_dir.rglob("*"):
        if not folder.is_dir():
            continue

        if folder.name.startswith("Moment_"):
            continue

        if contains_images(folder):
            time_sort(folder)

    print("Sorting completed!")