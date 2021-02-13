#! /usr/bin/env python

import json
import mimetypes
import os
import re

import gimp
from gimpfu import *

from lib import (
    guess_extension,
    guess_mimetype,
    listfiles,
)

QUALITY_FACTOR = 0.90
LOSSY = QUALITY_FACTOR < 1

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

MIMETYPE_SAVE_FUNC_MAP = {
    'image/webp': save_webp,
    'image/png': save_png
}

def run(
        src_dir,
        input_filename_regex,
        dest_dir,
        output_filename_template,
        mimetypes,
        widths,
        overwrite,
        show_skipped
    ):
    """Generate derivatives as required by derekenos.com-generator
    github.com/derekenos/derekenos.com-generator
    """
    INPUT_FILENAME_REGEX = re.compile(input_filename_regex)
    for filename, file_path in listfiles(src_dir):
        # Ignore non-image files.
        if not guess_mimetype(filename).startswith('image/'):
            continue

        # Parse the required fields from the filename.
        match_d = INPUT_FILENAME_REGEX.match(filename).groupdict()
        item_name = match_d['item_name']
        asset_id = match_d['asset_id']
        orig_width = int(match_d['width'])

        # Open the image.
        image = pdb.gimp_file_load(file_path, filename)

        # Sort widths descending.
        widths = sorted(widths, reverse=True)

        # If any requested widths are larger than the original image,
        # add the original width to the list and drop the larger values.
        i = next(i for i, width in enumerate(widths) if width < image.width)
        if i > 0:
            widths = [image.width] + widths[i:]

        for width in widths:
            if image.width > width:
                # Scale image down to width.
                height = int(float(width) / image.width * image.height)
                pdb.gimp_image_scale(image, width, height)

            for mimetype in mimetypes:
                out_fn = output_filename_template.format(
                    item_name=item_name,
                    asset_id=asset_id,
                    width=width,
                    extension=guess_extension(mimetype)
                )
                out_path = os.path.join(dest_dir, out_fn)
                # Skip path if overwrite is False and file already exists.
                if not overwrite and os.path.exists(out_path):
                    if show_skipped:
                        print('Skipping: {}'.format(out_path))
                    continue
                # Invoke either a custom or default save function.
                MIMETYPE_SAVE_FUNC_MAP.get(mimetype, pdb.gimp_file_save)(
                    image,
                    image.active_drawable,
                    out_path,
                    out_fn
                )
                print('Wrote: {}'.format(out_path))
