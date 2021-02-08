
import argparse
import json
import os
import subprocess
from glob import glob

def print_header(s):
    print(f'{"*" * 79}\n{s}\n{"*" * 79}')

def exec_gimp_normalize_item_image_filenames(input_path, template, item_name,
                                             output_path):
    """Given Execute the Gimp normalize_item_image_filenames script.
    """
    return subprocess.call((
        'flatpak',
        'run',
        'org.gimp.GIMP',
        '-idf',
        '--batch-interpreter',
        'python-fu-eval',
        '-b',
        f"import sys; sys.path = ['.'] + sys.path; import normalize_item_image_filenames; normalize_item_image_filenames.run('{input_path}', '{item_name}', '{template}', '{output_path}')",
        '-b',
        'pdb.gimp_quit(1)'
    ))

def exec_gimp_generate_derivatives(input_path, output_path, formats, widths,
                                   overwrite, show_skipped):
    """Execute the Gimp generate_derivatives script.
    """
    return subprocess.call((
        'flatpak',
        'run',
        'org.gimp.GIMP',
        '-idf',
        '--batch-interpreter',
        'python-fu-eval',
        '-b',
        f"import sys; sys.path = ['.'] + sys.path; import generate_derivatives; generate_derivatives.run('{input_path}', '{output_path}', {formats}, {widths}, {overwrite}, {show_skipped})",
        '-b',
        'pdb.gimp_quit(1)'
    ))

def exec_vlc(path, output_path):
    """Execute VLC to generate video poster images.
    """
    return subprocess.call((
        'vlc',
        path,
        '--rate=1',
        '--video-filter=scene',
        '--vout=dummy',
        '--start-time=0',
        '--stop-time=1',
        '--scene-format=png',
        '--scene-ratio=240',
        '--scene-prefix=snap',
        f'--scene-path={output_path}',
        '--scene-replace',
        '--quiet',
        'vlc://quit'
    ))

def normalize_item_image_filenames(input_path, context_file, item_name,
                                   output_path):
    # If an output path was not specified, write to {input_path}/normalized.
    if output_path is None:
        output_path = os.path.join(input_path, 'normalized')
    # Create the output directory if necessary.
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Read the normalized filename format from the context file.
    context = json.load(open(context_file, 'rb'))
    template = context['normalized_image_filename_template']

    print_header('Normalize item image filenames')
    res = exec_gimp_normalize_item_image_filenames(
        input_path,
        template,
        item_name,
        output_path
    )
    if res != 0:
        raise AssertionError(
            'Gimp normalize_item_image_filenames exited with a non-zero code'
        )

def generate_derivatives(input_path, context_file, output_path=None,
                         overwrite=False, show_skipped=False):
    # If output_path was not specified, write to {input_path}/derivatives.
    if output_path is None:
        output_path = os.path.join(input_path, 'derivatives')
    # Create the output directory if necessary.
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Read the configured formats and widths from context file.
    context = json.load(open(context_file, 'rb'))
    formats = context['prioritized_derivative_image_formats']
    widths = context['derivative_image_widths']

    # Execute the Gimp script.
    print_header('Generate image derivatives')
    res = exec_gimp_generate_derivatives(input_path, output_path, formats,
                                         widths, overwrite, show_skipped)
    if res != 0:
        raise AssertionError(
            'Gimp generate_derivatives exited with a non-zero code'
        )

    # Use vlc to generate video poster images.
    # https://wiki.videolan.org/VLC_HowTo/Make_thumbnails/
    # Only process MP4s for now.
    for ext in ('mp4',):
        print_header(f'Generate video poster images for type: {ext}')
        for path in glob(os.path.join(input_path, f'*.{ext}')):
            base_filename = os.path.splitext(os.path.basename(path))[0]
            final_path = f'{output_path}/{base_filename}_{ext}_poster.png'
            # Skip path if overwrite is False and file already exists.
            if not overwrite and os.path.exists(final_path):
                if show_skipped:
                    print(f'Skipping: {path}')
                continue
            res = exec_vlc(path, output_path)
            if res != 0:
                raise AssertionError(
                    f'Could not generate poster image for video: {path}'
                )

            # Rename the output file to reflect the input.
            os.rename(f'{output_path}/snap.png', final_path)
            print(f'Wrote: {final_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--context-file', type=str, default='context.json')
    subparsers = parser.add_subparsers(dest='action', required=True)

    norm_parser = subparsers.add_parser('normalize-item-image-filenames')
    norm_parser.add_argument('input_path', type=str)
    norm_parser.add_argument('item_name', type=str)
    norm_parser.add_argument('--output-path', type=str)

    gen_parser = subparsers.add_parser('generate-derivatives')
    gen_parser.add_argument('input_path', type=str)
    gen_parser.add_argument('--output-path', type=str)
    gen_parser.add_argument('--overwrite', action='store_true')
    gen_parser.add_argument('--show-skipped', action='store_true')
    args = parser.parse_args()

    if args.action == 'normalize-item-image-filenames':
        normalize_item_image_filenames(
            args.input_path,
            args.context_file,
            args.item_name,
            args.output_path
        )
    else:
        generate_derivatives(
            args.input_path,
            args.context_file,
            args.output_path,
            args.overwrite,
            args.show_skipped
        )
