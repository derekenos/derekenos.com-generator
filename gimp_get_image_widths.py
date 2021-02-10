#! /usr/bin/env python

import json
import mimetypes
import os

import gimp
from gimpfu import pdb

from lib import guess_mimetype

def run(src_dir, output_file):
    """For all image files in src_dir, create a filename => width map
    and write it as JSON to the output_file.
    """
    filename_width_map = {}
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue

        # Ignore non-image files.
        if not guess_mimetype(filename).startswith('image/'):
            continue

        # Open the image and read the width.
        width = pdb.gimp_file_load(file_path, filename).width
        filename_width_map[filename] = width

    with open(output_file, 'wb') as fh:
        fh.write(json.dumps(filename_width_map))
