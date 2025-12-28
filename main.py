"""
TO DO

1) Extract datetime object from image metadata
2) Extract GPS from image metadata
"""

from app import metadata

def main():
    timedate = metadata.get_datetime("images/img1.jpg")
    print(timedate.date())
    print(timedate.time())

    gps = metadata.get_gps("images/img1.jpg")
    print(gps)

if __name__ == "__main__":
    main()