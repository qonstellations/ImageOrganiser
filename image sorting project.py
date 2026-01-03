from pathlib import Path
from PIL import Image
import sys
print(sys.executable)
#print(list(Path.cwd().glob("*.jpg")))
for image_path in Path.cwd().glob("*.jpg"):
        print(image_path.name, end="\n")
        
