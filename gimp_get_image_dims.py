#! /usr/bin/env python

import json
import mimetypes
import os

from lib import guess_mimetype

from gi.repository import Gimp, Gio

to_bytes = lambda s: bytes(s, encoding="utf8")


def run(src_dir, output_file):
    """For all image files in src_dir, create a filename => (width, height) map
    and write it as JSON to the output_file.
    """
    filename_dims_map = {}
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue

        # Ignore non-image files.
        if not guess_mimetype(filename).startswith("image/"):
            continue

        # Open the image and read the width.
        g_file = Gio.File.new_for_path(to_bytes(file_path))
        image = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, g_file)
        filename_dims_map[filename] = image.get_width(), image.get_height()

    with open(output_file, "wb") as fh:
        fh.write(to_bytes(json.dumps(filename_dims_map)))
