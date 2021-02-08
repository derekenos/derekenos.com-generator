#! /usr/bin/env python

import json
import os
import re
from glob import glob

import gimp
from gimpfu import *

QUALITY_FACTOR = 0.90
LOSSY = QUALITY_FACTOR < 1

INPUT_FILENAME_GLOB = '*_original.*'
INPUT_FILENAME_REGEX = re.compile('^(?P<base_name>.*)_original\..*$')

get_output_filename = lambda base_name, width, ext: \
    '{0}_{1}.{2}'.format(base_name, width, ext)

def save_webp(image, drawable, path, filename):
    pdb.file_webp_save(
        image,
        drawable,
        path,
        filename,
        0, # preset=default
        0 if LOSSY else 1, # lossless
        100 * QUALITY_FACTOR, # quality,
        100, # alpha quality
        0, # use layers for animation
        0, # loop indefinitely
        0, # minimum animation size
        0, # max distance between keyframes
        1, # save exif data
        1, # save iptc data (whatever that is)
        1, # same xmp data (whatever that is)
        0, # delay to use when timestamps not available
        0, # force delay on all frames
    )

def save_png(image, drawable, path, filename):
    pdb.file_png_save(
        image,
        drawable,
        path,
        filename,
        0 if LOSSY else 1, # use adam7 interlacing
        9 - int(9 * QUALITY_FACTOR), # deflate compression factor,
        1, # write bKGD chunk
        1, # write gAMA chunk
        1, # write oFFs chunk
        1, # write pHYs chunk
        1, # write tIME chunk
    )

FORMAT_CUSTOM_SAVE_FUNC_MAP = {
    'webp': save_webp,
    'png': save_png
}

def run(src_dir, dest_dir, formats, widths, overwrite, show_skipped):
    """Generate derivatives as required by derekenos.com-generator
    github.com/derekenos/derekenos.com-generator
    """
    for path in glob(os.path.join(src_dir, INPUT_FILENAME_GLOB)):
        filename = os.path.basename(path)
        match = INPUT_FILENAME_REGEX.match(filename)
        base_name = match.group('base_name')
        image = pdb.gimp_file_load(path, filename)
        # Iterate over widths in descending order.
        for width in sorted(widths, reverse=True):
            if image.width < width:
                # Image is smaller than width so ignore this width.
                continue

            if image.width > width:
                # Scale image down to width.
                height = int(float(width) / image.width * image.height)
                pdb.gimp_image_scale(image, width, height)

            for fmt in formats:
                out_fn = get_output_filename(base_name, width, fmt)
                out_path = os.path.join(dest_dir, out_fn)
                # Skip path if overwrite is False and file already exists.
                if not overwrite and os.path.exists(out_path):
                    if show_skipped:
                        print('Skipping: {}'.format(out_path))
                    continue
                FORMAT_CUSTOM_SAVE_FUNC_MAP.get(fmt, pdb.gimp_file_save)(
                    image,
                    image.active_drawable,
                    out_path,
                    out_fn
                )
                print('Wrote: {}'.format(out_fn))
