
import argparse
import json
import mimetypes
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict

def print_header(s):
    print(f'{"*" * 79}\n{s}\n{"*" * 79}')

def guess_type(path):
    """Define a mimetypes.guess_type() wrapper that also
    handles webp.
    """
    if path.endswith('.webp'):
        return ('image/webp', None)
    return mimetypes.guess_type(path)

def call_subprocess(args, **kwargs):
    """A subprocess.call() helper that captures stderr and raises an
    exception on non-zero exit.
    """
    stderr_fh = tempfile.TemporaryFile()
    res = subprocess.call(
        args,
        stderr=stderr_fh,
        **kwargs
    )
    if res != 0:
        stderr_fh.seek(0)
        raise AssertionError(f'Subprocess Error: {stderr_fh.read()}')

def get_image_widths(input_path):
    """Return a filename -> width map for all image files in input_path.
    """
    # Execute a Gimp script that collects image file widths and writes a
    # JSON filename -> width map to a specified file.
    with tempfile.NamedTemporaryFile() as fh:
        args = (
            'flatpak',
            'run',
            'org.gimp.GIMP',
            '-idf',
            '--batch-interpreter',
            'python-fu-eval',
            '-b',
            f"import sys; sys.path = ['.'] + sys.path; import gimp_get_image_widths; gimp_get_image_widths.run('{input_path}', '{fh.name}')",
            '-b',
            'pdb.gimp_quit(1)'
        )
        call_subprocess(args, stdout=subprocess.DEVNULL)
        # Load the written data from the file.
        fh.seek(0)
        filename_width_map = json.load(fh)
    return filename_width_map

def generate_image_derivatives(
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
    call_subprocess((
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

def generate_video_poster(path, output_path):
    """Execute VLC to generate a video poster image.
    """
    call_subprocess((
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

def assert_no_unhandled_mime_types(input_path):
    """Assert that input_path contains no unhandled files.
    """
    unhandled_mime_filenames_map = defaultdict(list)
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue
        mime = guess_type(file_path)[0]
        if mime is None or (
                not mime.startswith('image/')
                and not mime.startswith('video/')
            ):
            unhandled_mime_filenames_map[mime].append(filename)
    if unhandled_mime_filenames_map:
        raise AssertionError(
            'Directory contains files of unknown or unhandled mime types: '
            + str(dict(unhandled_mime_filenames_map))
        )

def generate_video_derivatives(
        input_path,
        poster_filename_template,
        output_path,
        overwrite,
        show_skipped
    ):
    """Use vlc to generate video poster images.
    https://wiki.videolan.org/VLC_HowTo/Make_thumbnails/
    """
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue
        # Ignore non-video files.
        if not guess_type(file_path)[0].startswith('video/'):
            continue

        poster_filename = poster_filename_template.format(
            base_filename=os.path.splitext(filename)[0]
        )
        final_path = os.path.join(output_path, poster_filename)
        # Skip path if overwrite is False and file already exists.
        if not overwrite and os.path.exists(final_path):
            if show_skipped:
                print(f'Skipping: {file_path}')
            continue
        generate_video_poster(file_path, output_path)

        # Rename the output file to reflect the input.
        os.rename(os.path.join(output_path, 'snap.png'), final_path)
        print(f'Wrote: {final_path}')

def normalize_item_filenames(input_path, context_file, item_name, output_path):
    # Assert that we can handle all the files in input_path.
    assert_no_unhandled_mime_types(input_path)

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

    # Get an image filename -> width map.
    print_header('Reading image widths...')
    image_filename_width_map = get_image_widths(input_path)

    print_header('Normalizing item filenames')
    for i, filename in enumerate(os.listdir(input_path), 1):
        file_path = os.path.join(input_path, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue

        # Use the appropriate template to generate the normalized filename.
        extension = os.path.splitext(filename)[1].lstrip('.')
        mime = guess_type(file_path)[0]
        if mime.startswith('image/'):
            normalized_filename = image_template.format(
                item_name=item_name,
                file_num=i,
                width=image_filename_width_map[filename],
                extension=extension
            )
        elif mime.startswith('video/'):
            normalized_filename = video_template.format(
                item_name=item_name,
                file_num=i,
                extension=extension
            )

        # Do the copy.
        new_path = os.path.join(output_path, normalized_filename)
        shutil.copy(file_path, new_path)
        print('Normalized {} to {}'.format(filename, normalized_filename))

def generate_derivatives(
        input_path,
        context_file,
        output_path=None,
        overwrite=False,
        show_skipped=False
    ):
    # Assert that we can handle all the files in input_path.
    assert_no_unhandled_mime_types(input_path)

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

    # Generate image derivatives.
    print_header('Generate image derivatives')
    generate_image_derivatives(
        input_path,
        input_filename_regex,
        output_path,
        output_filename_template,
        formats,
        widths,
        overwrite,
        show_skipped
    )

    # Generate video derivatives.
    print_header('Generate video poster images')
    generate_video_derivatives(
        input_path,
        video_poster_filename_template,
        output_path,
        overwrite,
        show_skipped
    )

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
