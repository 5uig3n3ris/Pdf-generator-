import os
import urllib.request

font_dir = "fonts"
font_url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf"
font_path = os.path.join(font_dir, "DejaVuSans.ttf")

os.makedirs(font_dir, exist_ok=True)
print("Downloading font...")
urllib.request.urlretrieve(font_url, font_path)
print("Font downloaded to", font_path)
