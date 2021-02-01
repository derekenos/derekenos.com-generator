#! /usr/bin/env python

import os
import re
from glob import glob

import gimp
from gimpfu import *

INPUT_FILENAME_GLOB = '*_original.*'
INPUT_FILENAME_REGEX = re.compile('(?:.+/)(?P<base_name>.*)_original\.(?P<extension>.*)')

get_output_filename = lambda base_name, width, ext: \
    '{0}_{1}.{2}'.format(base_name, width, ext)

# Define the list of derivative widths to generate.
# Taken from: https://support.squarespace.com/hc/en-us/articles/206542517-Formatting-your-images-for-display-on-the-web
WIDTHS = (
    100,
    300,
    500,
    750,
    1000,
    1500,
    2500
)

def run(src_dir, dest_dir):
    """Generate derivatives as required by derekenos.com-generator
    github.com/derekenos/derekenos.com-generator
    """
    for path in glob(os.path.join(src_dir, INPUT_FILENAME_GLOB)):
        print('src: {}'.format(path))

        match = INPUT_FILENAME_REGEX.match(path)
        base_name = match.group('base_name')
        extension = match.group('extension')

        for width in WIDTHS:
            out_fn = get_output_filename(base_name, width, extension)
            print('derivative: {}'.format(out_fn))
