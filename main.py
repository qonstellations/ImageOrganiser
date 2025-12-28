"""
TO DO

1) Extract datetime object from image metadata - DONE
2) Extract GPS from image metadata - DONE
3) Sort photos according to their datetime objects (year, month, day)
"""

from app import metadata
from pathlib import Path

def main():
    # Code to check all data
    for i in range(1, 4):
        path = Path(f"images/img{i}.jpg")
        timedate = metadata.get_datetime(path)
        gpsdata = metadata.get_gps(path)

        print(f"\nImage {i}")
        print(timedate.date(), timedate.time())
        print(gpsdata)

if __name__ == "__main__":
    main()