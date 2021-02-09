#! /usr/bin/env python

import json
import mimetypes
import os

import gimp
from gimpfu import pdb

def run(src_dir, output_file):
    """For all image files in src_dir, create a filename => width map
    and write it as JSON to the output_file.
    """
    filename_width_map = {}
    for i, filename in enumerate(os.listdir(src_dir)):
        file_path = os.path.join(src_dir, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue

        # Attempt to determine the mime type.
        mime = mimetypes.guess_type(filename)[0]
        # Raise an exception if detection failed.
        if mime is None:
            raise AssertionError(
                'Could not guess MIME type for filename: {}'.format(filename)
            )
        # Ignore non-image files.
        if not mime.startswith('image/'):
            continue

        # Open the image and read the width.
        width = pdb.gimp_file_load(file_path, filename).width
        filename_width_map[filename] = width

    with open(output_file, 'wb') as fh:
        fh.write(json.dumps(filename_width_map))
