
import argparse
import json
import mimetypes
import os
import subprocess
from glob import glob

def print_header(s):
    print(f'{"*" * 79}\n{s}\n{"*" * 79}')

def exec_gimp_normalize_item_filenames(
        input_path,
        image_template,
        video_template,
        item_name,
        output_path
    ):
    """Given Execute the Gimp normalize_item_filenames script.
    """
    return subprocess.call((
        'flatpak',
        'run',
        'org.gimp.GIMP',
        '-idf',
        '--batch-interpreter',
        'python-fu-eval',
        '-b',
        f"import sys; sys.path = ['.'] + sys.path; import gimp_normalize_item_filenames; gimp_normalize_item_filenames.run('{input_path}', '{item_name}', '{image_template}', '{video_template}', '{output_path}')",
        '-b',
        'pdb.gimp_quit(1)'
    ))

def exec_gimp_generate_derivatives(
        input_path,
        input_filename_regex,
        output_path,
        output_filename_template,
        formats,
        widths,
        overwrite,
        show_skipped
    ):
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
        f"import sys; sys.path = ['.'] + sys.path; import gimp_generate_derivatives; gimp_generate_derivatives.run('{input_path}', '{input_filename_regex}', '{output_path}', '{output_filename_template}', {formats}, {widths}, {overwrite}, {show_skipped})",
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

def normalize_item_filenames(input_path, context_file, item_name, output_path):
    # If an output path was not specified, write to {input_path}/normalized.
    if output_path is None:
        output_path = os.path.join(input_path, 'normalized')
    # Create the output directory if necessary.
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Read the normalized filename format from the context file.
    context = json.load(open(context_file, 'rb'))
    image_template = context['normalized_image_filename_template']
    video_template = context['normalized_video_filename_template']

    print_header('Normalize item image filenames')
    res = exec_gimp_normalize_item_filenames(
        input_path,
        image_template,
        video_template,
        item_name,
        output_path
    )
    if res != 0:
        raise AssertionError(
            'Gimp normalize_item_filenames exited with a non-zero code'
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
    input_filename_regex = context['normalized_image_filename_regex']
    output_filename_template = context['derivative_image_filename_template']
    video_poster_filename_template = context[
        'derivative_video_poster_filename_template'
    ]

    # Execute the Gimp script.
    print_header('Generate image derivatives')
    res = exec_gimp_generate_derivatives(
        input_path,
        input_filename_regex,
        output_path,
        output_filename_template,
        formats,
        widths,
        overwrite,
        show_skipped
    )
    if res != 0:
        raise AssertionError(
            'Gimp generate_derivatives exited with a non-zero code'
        )

    # Use vlc to generate video poster images.
    # https://wiki.videolan.org/VLC_HowTo/Make_thumbnails/
    # Only process MP4s for now.
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue
        # Ignore non-video files.
        mime = mimetypes.guess_type(file_path)[0]
        if mime is None:
            raise AssertionError(
                'Could not guess MIME type for filename: {}'.format(filename)
            )
        if not mime.startswith('video/'):
            continue

        poster_filename = video_poster_filename_template.format(
            base_filename=os.path.splitext(filename)[0]
        )
        final_path = os.path.join(output_path, poster_filename)
        # Skip path if overwrite is False and file already exists.
        if not overwrite and os.path.exists(final_path):
            if show_skipped:
                print(f'Skipping: {file_path}')
            continue
        res = exec_vlc(file_path, output_path)
        if res != 0:
            raise AssertionError(
                f'Could not generate poster image for video: {path}'
            )

        # Rename the output file to reflect the input.
        os.rename(os.path.join(output_path, 'snap.png'), final_path)
        print(f'Wrote: {final_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--context-file', type=str, default='context.json')
    subparsers = parser.add_subparsers(dest='action', required=True)

    norm_parser = subparsers.add_parser('normalize-item-filenames')
    norm_parser.add_argument('input_path', type=str)
    norm_parser.add_argument('item_name', type=str)
    norm_parser.add_argument('--output-path', type=str)

    gen_parser = subparsers.add_parser('generate-derivatives')
    gen_parser.add_argument('input_path', type=str)
    gen_parser.add_argument('--output-path', type=str)
    gen_parser.add_argument('--overwrite', action='store_true')
    gen_parser.add_argument('--show-skipped', action='store_true')
    args = parser.parse_args()

    if args.action == 'normalize-item-filenames':
        normalize_item_filenames(
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
