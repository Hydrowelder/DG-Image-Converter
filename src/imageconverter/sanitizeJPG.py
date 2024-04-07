from pathlib import Path
import os
import numpy as np
import shutil


def sanitizeJPG(jpgs:str, target:str, raws:str=".", raw_format:str=".ARW", jpg_format:str='.JPG'):
    raws = Path(raws)
    jpgs = Path(jpgs)
    Path(target).mkdir(parents=True, exist_ok=True)
    target = Path(target)
    
    raws_files = list(raws.glob("*"+raw_format))
    for i in range(len(raws_files)):
        raw_file = raws_files[i]
        jpg_file = Path(jpgs,raw_file.stem+jpg_format)

        shutil.copy(jpg_file,target)


if __name__ == "__main__":
    root="/Users/davidgable/Pictures/Starlink 8-1"
    sanitizeJPG(jpgs=root+'/JPG',target=root+'/JPGout',raws=root+'/RAW')
