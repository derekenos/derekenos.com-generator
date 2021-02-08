#! /usr/bin/env python

import os
import shutil
from glob import glob

import gimp
from gimpfu import *

def run(src_dir, item_name, template, dest_dir):
    """Given a path to image assets for a single item, copy the files to
    a {src_dir}/normalized subdirectory with a filename that conforms with the
    format specified by the normalized_image_filename_format context field.
    """
    for i, filename in enumerate(os.listdir(src_dir)):
        path = os.path.join(src_dir, filename)
        # Ignore non-normal-file entries.
        if not os.path.isfile(path):
            continue
        # Read the image width.
        image = pdb.gimp_file_load(path, filename)
        width = image.width
        ext = os.path.splitext(filename)[1].lstrip('.')
        new_filename = template.format(
            item_name=item_name,
            file_num=i,
            width=width,
            extension=ext
        )
        new_path = os.path.join(dest_dir, new_filename)
        shutil.copy(path, new_path)
        print('Normalized {} to {}'.format(filename, new_filename))
