

from pathlib import Path
from PIL import Image

print("Current working directory:", Path.cwd())

for image_path in Path.cwd().glob("*.jpg"):
    print(image_path.name)

for p in Path.cwd().iterdir():
    print(p.name, "=> suffix:", p.suffix)
