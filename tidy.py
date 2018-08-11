#!/usr/bin/env python3
import os
import shutil

DOWNLOADS = os.path.expanduser('~/Downloads')
PICTURES = os.path.expanduser('~/Pictures/unsorted')

for name in os.listdir(DOWNLOADS):
    if name.lower().endswith(('.jpg', '.png')):
        shutil.move(os.path.join(DOWNLOADS, name), os.path.join(PICTURES, name))
        print('moved', name)
