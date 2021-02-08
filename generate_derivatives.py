#! /usr/bin/env python

import json
import os
import re
from glob import glob

import gimp
from gimpfu import *

INPUT_FILENAME_GLOB = '*_original.*'
INPUT_FILENAME_REGEX = re.compile('^(?P<base_name>.*)_original\..*$')

get_output_filename = lambda base_name, width, ext: \
    '{0}_{1}.{2}'.format(base_name, width, ext)

def run(src_dir, dest_dir, formats, widths):
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
                pdb.gimp_file_save(
                    image,
                    image.active_drawable,
                    os.path.join(dest_dir, out_fn),
                    out_fn
                )
                print('Wrote: {}'.format(out_fn))
