import os
from os import path
import shutil

src = "/Users/cp/Documents/dsi/8a_project/8a_scraper"
dst = "/Volumes/data"

files = [i for i in os.listdir(src) if i.startswith("data-") and path.isfile(path.join(src, i))]
for f in files:
    shutil.copy(path.join(src, f), dst)