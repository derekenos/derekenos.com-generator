#! /usr/bin/env python

import mimetypes
import os
import shutil
from glob import glob

import gimp
from gimpfu import *

def run(src_dir, item_name, image_template, video_template, dest_dir):
    """Given a path to image assets for a single item, copy the files to
    a {src_dir}/normalized subdirectory with a filename that conforms with the
    format specified by the normalized_image_filename_format context field.
    """
    for i, filename in enumerate(os.listdir(src_dir)):
        file_path = os.path.join(src_dir, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue
        # Ignore non-normal-file entries.
        if not os.path.isfile(path):
            continue

        # Determine the asset type.
        mime = mimetypes.guess_type(filename)[0]
        if mime is None:
            raise AssertionError(
                'Could not guess MIME type for filename: {}'.format(filename)
            )
        asset_type = mime.split('/')[0]

        # use the appropriate template to generate the new filename.
        extension = os.path.splitext(filename)[1].lstrip('.')
        if asset_type == 'image':
            image = pdb.gimp_file_load(file_path, filename)
            width = image.width
            new_filename = image_template.format(
                item_name=item_name,
                file_num=i,
                width=width,
                extension=extension
            )
        elif asset_type == 'video':
            new_filename = video_template.format(
                item_name=item_name,
                file_num=i,
                extension=extension
            )
        else:
            raise NotImplemented(asset_type)

        new_path = os.path.join(dest_dir, new_filename)
        shutil.copy(file_path, new_path)
        print('Normalized {} to {}'.format(filename, new_filename))
