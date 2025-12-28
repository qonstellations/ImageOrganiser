"""
TO DO

1) Extract datetime object from image metadata
2) Extract GPS from image metadata
"""

from app import metadata

def main():
    metadata.get_datetime("images/img1.jpg")

if __name__ == "__main__":
    main()