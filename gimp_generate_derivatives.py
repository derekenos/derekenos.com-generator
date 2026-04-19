#! /usr/bin/env python

import json
import mimetypes
import os
import re

from gi.repository import Gimp, Gio

from lib import (
    guess_extension,
    guess_mimetype,
    listfiles,
)

QUALITY_FACTOR = 0.90
LOSSY = QUALITY_FACTOR < 1

to_bytes = lambda s: bytes(s, encoding="utf8")


def save_image(image, out_path, options=None):
    Gimp.file_save(
        run_mode=Gimp.RunMode.NONINTERACTIVE,
        image=image,
        file=Gio.File.new_for_path(to_bytes(out_path)),
        options=options,
    )


def save_webp(image, out_path):
    save_image(
        image,
        out_path,
    )
    #     0, # preset=default
    #     0 if LOSSY else 1, # lossless
    #     100 * QUALITY_FACTOR, # quality,
    #     100, # alpha quality
    #     0, # use layers for animation
    #     0, # loop indefinitely
    #     0, # minimum animation size
    #     0, # max distance between keyframes
    #     1, # save exif data
    #     1, # save iptc data (whatever that is)
    #     1, # same xmp data (whatever that is)
    #     0, # delay to use when timestamps not available
    #     0, # force delay on all frames
    # )


def save_png(image, out_path):
    save_image(
        image,
        out_path,
    )

    #     0 if LOSSY else 1, # use adam7 interlacing
    #     9 - int(9 * QUALITY_FACTOR), # deflate compression factor,
    #     1, # write bKGD chunk
    #     1, # write gAMA chunk
    #     1, # write oFFs chunk
    #     1, # write pHYs chunk
    #     1, # write tIME chunk
    # )


def save_jpg(image, out_path):
    proc = Gimp.get_pdb().lookup_procedure("file-jpeg-export")
    conf = proc.create_config()
    conf.set_property("run-mode", Gimp.RunMode.NONINTERACTIVE)
    conf.set_property("image", image)
    conf.set_property("file", Gio.File.new_for_path(to_bytes(out_path)))
    conf.set_property("quality", QUALITY_FACTOR)
    # How to set these?
    # 0.10, # smoothing (whatever that is)
    # 1, # optimize
    # 1, # progressive
    # '', # comment
    # 1, # subsmp
    # 0, # baseline
    # 16, # restart (apparent default in Gimp UI)
    # 0, # DCT
    return proc.run(conf)


MIMETYPE_SAVE_FUNC_MAP = {
    "image/webp": save_webp,
    "image/png": save_png,
    "image/jpeg": save_jpg,
}


def run(
    src_dir,
    input_filename_regex,
    dest_dir,
    output_filename_template,
    mimetypes,
    widths,
    overwrite,
    show_skipped,
):
    """Generate derivatives as required by derekenos.com-generator
    github.com/derekenos/derekenos.com-generator
    """
    INPUT_FILENAME_REGEX = re.compile(input_filename_regex)

    # Ensure that widths are sorted descending.
    widths = sorted(widths, reverse=True)
    for filename, file_path in listfiles(src_dir):
        # Ignore non-image files.
        if not guess_mimetype(filename).startswith("image/"):
            continue

        # Parse the required fields from the filename.
        match_d = INPUT_FILENAME_REGEX.match(filename).groupdict()
        item_name = match_d["item_name"]
        asset_id = match_d["asset_id"]
        orig_width = int(match_d["width"])

        # Open the image.
        g_file = Gio.File.new_for_path(to_bytes(file_path))
        image = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, g_file)

        # If any requested widths are larger than the original image,
        # add the original width to the list and drop the larger values.
        image_width = image.get_width()
        i = next(i for i, width in enumerate(widths) if width < image_width)
        final_widths = [image_width] + widths[i:] if i > 0 else widths

        image_height = image.get_height()
        for width in final_widths:
            if image_width > width:
                # Scale image down to width.
                scale = float(width) / image_width
                height = int(image_height * scale)
                image.scale(width, height)

            for mimetype in mimetypes:
                out_fn = output_filename_template.format(
                    item_name=item_name,
                    asset_id=asset_id,
                    width=width,
                    extension=guess_extension(mimetype),
                )
                out_path = os.path.join(dest_dir, out_fn)
                # Skip path if overwrite is False and file already exists.
                if not overwrite and os.path.exists(out_path):
                    if show_skipped:
                        print("Skipping: {}".format(out_path))
                    continue
                # Invoke either a custom or default save function.
                MIMETYPE_SAVE_FUNC_MAP.get(mimetype, save_image)(
                    image,
                    out_path,
                )
                print("Wrote: {}".format(out_path))
