
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict

from lib import guess_mimetype

###############################################################################
# Helper Functions
###############################################################################

def print_header(s):
    print(f'{"*" * 79}\n{s}\n{"*" * 79}')

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

def assert_no_unhandled_mimetypes(input_path):
    """Assert that input_path contains no unhandled files.
    """
    unhandled_mimetype_filenames_map = defaultdict(list)
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue
        mimetype = guess_mimetype(file_path)
        if mimetype is None or (
                not mimetype.startswith('image/')
                and not mimetype.startswith('video/')
            ):
            unhandled_mimetype_filenames_map[mimetype].append(filename)
    if unhandled_mimetype_filenames_map:
        raise AssertionError(
            'Directory contains files of unknown or unhandled mimetypes: '
            + str(dict(unhandled_mimetype_filenames_map))
        )

###############################################################################
# Item Filename Normalization Functions
###############################################################################

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

def normalize_item_filenames(input_path, context_file, item_name, output_path):
    # Assert that we can handle all the files in input_path.
    assert_no_unhandled_mimetypes(input_path)

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
    file_num = 0
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        # Ignore directories.
        if os.path.isdir(file_path):
            continue
        # Increment the file number.
        file_num += 1

        # Use the appropriate template to generate the normalized filename.
        extension = os.path.splitext(filename)[1]
        mimetype = guess_mimetype(file_path)
        if mimetype.startswith('image/'):
            normalized_filename = image_template.format(
                item_name=item_name,
                file_num=file_num,
                width=image_filename_width_map[filename],
                extension=extension
            )
        elif mimetype.startswith('video/'):
            normalized_filename = video_template.format(
                item_name=item_name,
                file_num=file_num,
                extension=extension
            )

        # Do the copy.
        new_path = os.path.join(output_path, normalized_filename)
        shutil.copy(file_path, new_path)
        print('Normalized {} to {}'.format(filename, normalized_filename))

###############################################################################
# Derivative Generation Functions
###############################################################################

def generate_image_derivatives(
        input_path,
        input_filename_regex,
        output_path,
        output_filename_template,
        mimetypes,
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
        f"import sys; sys.path = ['.'] + sys.path; import gimp_generate_derivatives; gimp_generate_derivatives.run('{input_path}', '{input_filename_regex}', '{output_path}', '{output_filename_template}', {mimetypes}, {widths}, {overwrite}, {show_skipped})",
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
        if not guess_mimetype(file_path).startswith('video/'):
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

def generate_derivatives(
        input_path,
        context_file,
        output_path=None,
        overwrite=False,
        show_skipped=False
    ):
    # Assert that we can handle all the files in input_path.
    assert_no_unhandled_mimetypes(input_path)

    # If output_path was not specified, write to {input_path}/derivatives.
    if output_path is None:
        output_path = os.path.join(input_path, 'derivatives')
    # Create the output directory if necessary.
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Read the configured mimetypes and widths from context file.
    context = json.load(open(context_file, 'rb'))
    mimetypes = context['prioritized_derivative_image_mimetypes']
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
        mimetypes,
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

###############################################################################
# Add to Project
###############################################################################

def review_file(path, required_fields, viewer):
    """Launch the appropriate viewer application so the user may see the file
    and prompt for the required metadata.
    """
    # Launch the viewer.
    print(f'Opening viewer for: {path}')
    p = subprocess.Popen(
        (viewer, path),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Prompt for the metadata.
    print('Add metadata for this file')
    metadata = {}
    for field in required_fields:
        metadata[field] = input(f'Enter {field}: ')

    # If the viewer is still open, close it.
    if p.poll() is None:
        p.kill()
        p.wait()

    return metadata

def add_to_project(
        project_name,
        context_file,
        normalized_path,
        static_path,
        derivatives_path,
        image_viewer,
        video_viewer
    ):
    """Add the assets in the specified directories to an existing project in
    the context file.
    """
    if derivatives_path is None:
        derivatives_path = os.path.join(normalized_path, 'derivatives')

    # Read the context file and get the project.
    context = json.load(open(context_file, 'rb'))
    projects = [x for x in context['projects'] if x['name'] == project_name]
    num_matching_projects = len(projects)
    if num_matching_projects == 0:
        raise AssertionError(f'No project found for name: "{project_name}"')
    if num_matching_projects > 1:
        raise AssertionError(f'Multiple projects found for name: "{project_name}"')
    project = projects[0]

    # Assert that the project doesn't define any images or videos.
    if project.get('images') or project.get('videos'):
        raise AssertionError(
            f'Project "{project_name}" has existing defined images or videos'
        )

    # Define the required metadata fields.
    required_fields = ('name', 'description')

    # Start processing the normalized files.
    images = []
    videos = []
    for filename in (os.listdir(normalized_path)[0],):
        path = os.path.join(normalized_path, filename)
        mimetype = guess_mimetype(path)
        type = mimetype.split('/')[0]

        item = { 'filename': filename }
        item.update(
            review_file(
                path,
                required_fields,
                image_viewer if type == 'image' else video_viewer
            )
        )

        (images if type == 'image' else videos).append(item)

    # Update the project images.
    if images:
        project['images'] = images
    elif 'images' in project:
        del project['images']

    # Update the project videos.
    if videos:
        project['videos'] = videos
    elif 'videos' in project:
        del project['videos']

    # Update the context file.
    with open(context_file, 'w', encoding='utf-8') as fh:
        json.dump(context, fh, indent=2)

    print(f'Added {len(images)} images and {len(videos)} videos to '\
          f'"{project_name}"')

    # TODO - copy the files into the static directory.

###############################################################################
# CLI
###############################################################################

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

    add_to_project_parser = subparsers.add_parser('add-to-project')
    add_to_project_parser.add_argument('project_name', type=str)
    add_to_project_parser.add_argument(
        'normalized_path',
        type=str,
        help='The path to the directory containing the files generated by '\
        'normalize-item-filenames'
    )
    add_to_project_parser.add_argument(
        'static_path',
        type=str,
        help='The path to the directory containing your site\'s static assets'\
        ', to which the normalized and derivative files will be moved'
    )
    add_to_project_parser.add_argument(
        '--derivatives-path',
        type=str,
        help='The path to the directory containing the files generated by '\
        'generate-derivatives'
    )
    add_to_project_parser.add_argument('--image-viewer', default='exo-open')
    add_to_project_parser.add_argument('--video-viewer', default='vlc')

    args = parser.parse_args()

    if args.action == 'normalize-item-filenames':
        normalize_item_filenames(
            args.input_path,
            args.context_file,
            args.item_name,
            args.output_path
        )
    elif args.action == 'generate-derivatives':
        generate_derivatives(
            args.input_path,
            args.context_file,
            args.output_path,
            args.overwrite,
            args.show_skipped
        )
    else:
        add_to_project(
            args.project_name,
            args.context_file,
            args.normalized_path,
            args.static_path,
            args.derivatives_path,
            args.image_viewer,
            args.video_viewer
        )
