
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict

from lib import (
    listfiles,
    guess_mimetype,
    slugify,
)

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
    for filename, file_path in listfiles(input_path):
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

def normalize_item_filenames(context_file, input_path, item_name, output_path):
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
    for filename, file_path in listfiles(input_path):
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
        print(f'Normalized {file_path} to {new_path}')

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
    for filename, file_path in listfiles(input_path):
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
        context_file,
        input_path,
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

def review_file(path, field_default_pairs, viewer):
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
    for field, default in field_default_pairs:
        while True:
            if default:
                msg = f'Enter {field} (ENTER for "{default}"): '
            else:
                msg = f'Enter {field}: '
            value = input(msg)
            if value == '' and default is None:
                continue
            value = value if value else default
            break
        metadata[field] = value

    # If the viewer is still open, close it.
    if p.poll() is None:
        p.kill()
        p.wait()

    return metadata

def add_to_project(
        context_file,
        project_name,
        normalized_path,
        image_viewer,
        video_viewer,
        accept_defaults,
        overwrite
    ):
    """Add the assets in the specified directories to an existing project in
    the context file.
    """
    # Read the context file and get the project.
    context = json.load(open(context_file, 'rb'))
    projects = [x for x in context['projects'] if x['name'] == project_name]
    num_matching_projects = len(projects)
    if num_matching_projects == 0:
        raise AssertionError(f'No project found for name: "{project_name}"')
    if num_matching_projects > 1:
        raise AssertionError(
            f'Multiple projects found for name: "{project_name}"'
        )
    project = projects[0]

    # Assert that the project doesn't define any images or videos.
    if not overwrite and (project.get('images') or project.get('videos')):
        raise AssertionError(
            f'Project "{project_name}" has existing defined images or videos'
        )

    # Start processing the normalized files.
    images = []
    videos = []
    for filename, path in listfiles(normalized_path):
        mimetype = guess_mimetype(path)
        type = mimetype.split('/')[0]
        type_name = 'picture' if type == 'image' else 'movie'

        # Define the required metadata fields.
        field_default_pairs = (
            ('name', project_name),
            ('description', f'A {type_name} of the {project_name}')
        )

        item = { 'filename': filename }

        if accept_defaults:
            item.update(dict(field_default_pairs))
        else:
            item.update(
                review_file(
                    path,
                    field_default_pairs,
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

###############################################################################
# Auto
###############################################################################

def auto(
        context_file,
        assets_path,
        project_name,
        static_path,
        image_viewer,
        video_viewer,
        accept_defaults,
        overwrite
    ):

    # Normalize the asset filenames.
    norm_dir = tempfile.mkdtemp()
    item_name = f'project-{slugify(project_name)}'
    normalize_item_filenames(context_file, assets_path, item_name, norm_dir)

    # Generate the derivatives.
    deriv_dir = os.path.join(norm_dir, 'derivatives')
    generate_derivatives(context_file, norm_dir, deriv_dir)

    # Add to project.
    add_to_project(
        context_file,
        project_name,
        norm_dir,
        image_viewer,
        video_viewer,
        accept_defaults,
        overwrite
    )

    # Move the normalized and derivative files into the static dir.
    num_norm = 0
    for _, path in listfiles(norm_dir):
        shutil.move(path, static_path)
        num_norm += 1
    print(f'Moved {num_norm} files from {norm_dir} to {static_path}')

    num_deriv = 0
    for _, path in listfiles(deriv_dir):
        shutil.move(path, static_path)
        num_deriv += 1
    print(f'Moved {num_deriv} files from {deriv_dir} to {static_path}')

    # Remove the temp directories.
    os.rmdir(deriv_dir)
    os.rmdir(norm_dir)

###############################################################################
# CLI
###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--context-file', type=str, default='context.json')
    subparsers = parser.add_subparsers(dest='action', required=True)

    auto_parser = subparsers.add_parser('auto')
    auto_parser.add_argument('assets_path', type=str)
    auto_parser.add_argument('project_name', type=str)
    auto_parser.add_argument('static_path', type=str)
    auto_parser.add_argument('--image-viewer', default='exo-open')
    auto_parser.add_argument('--video-viewer', default='vlc')
    auto_parser.add_argument('--accept-defaults', action='store_true')
    auto_parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing project images and videos defined in context'
    )

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
    add_to_project_parser.add_argument('--image-viewer', default='exo-open')
    add_to_project_parser.add_argument('--video-viewer', default='vlc')
    add_to_project_parser.add_argument(
        '--accept-defaults',
        action='store_true'
    )
    add_to_project_parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing project images and videos defined in context'
    )

    add_to_project_parser = subparsers.add_parser('add-to-project')

    args = parser.parse_args()

    if args.action == 'auto':
        auto(
            args.context_file,
            args.assets_path,
            args.project_name,
            args.static_path,
            args.image_viewer,
            args.video_viewer,
            args.accept_defaults,
            args.overwrite
        )
    elif args.action == 'normalize-item-filenames':
        normalize_item_filenames(
            args.context_file,
            args.input_path,
            args.item_name,
            args.output_path
        )
    elif args.action == 'generate-derivatives':
        generate_derivatives(
            args.context_file,
            args.input_path,
            args.output_path,
            args.overwrite,
            args.show_skipped
        )
    else:
        add_to_project(
            args.context_file,
            args.project_name,
            args.normalized_path,
            args.image_viewer,
            args.video_viewer,
            args.accept_defaults,
            args.overwrite
        )
