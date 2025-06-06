
import os
import re
from collections import namedtuple
from datetime import datetime
from itertools import count

from lib import (
    large_static_store,
    microdata,
    guess_extension,
    guess_mimetype,
)

COLLATERAL_CREATIONS = 'collateral_creations'
DEPENDS_ON = 'depends_on'
DEPENDENT_OF = 'dependent_of'

###############################################################################
# Exceptions
###############################################################################

class InvalidContext(Exception): pass

###############################################################################
# Types
###############################################################################

ImageSource = namedtuple(
    'ImageSource',
    ('filename', 'mimetype', 'url', 'width', 'height', 'last_modified')
)

VideoSource = namedtuple(
    'VideoSource',
    ('filename', 'mimetype', 'url', 'last_modified', 'poster_url')
)

###############################################################################
# Helpers
###############################################################################

get_type_url = lambda x: f'https://schema.org/{x}'

###############################################################################
# Context Class
###############################################################################

class Context:
    """This class is used to represent the application state and provides
    methods for working with that state.
    """
    # Define the default static and site directories.
    PAGES_DIR = 'pages'
    STATIC_DIR = 'static'
    SITE_DIR = 'site'
    SITE_RELATIVE_STATIC_DIR = 'static'
    SITE_STATIC_DIR = f'{SITE_DIR}/{SITE_RELATIVE_STATIC_DIR}'
    STATIC_LARGE_FILE_THRESHOLD_KB = 0
    SITE_RELATIVE_LARGE_STATIC_DIR = f'static/_large'
    SITE_LARGE_STATIC_DIR = f'{SITE_DIR}/{SITE_RELATIVE_LARGE_STATIC_DIR}'
    SITEMAP_FILENAME = 'sitemap.txt'

    def __init__(self, production, **kwargs):
        self.production = production
        # Generate a list of page names in self.PAGES_DIR.
        self.page_names = [
            mod_name.rsplit('.', 1)[0]
            for mod_name in os.listdir(self.PAGES_DIR)
            if mod_name.endswith('.py')
        ]

        # Initialize runtime attributes.
        self.current_page = None
        self.current_page_mod = None
        self.generator_item = None

        # Maybe instantiate a large static store.
        lss_config = kwargs.get('large_static_store')
        self.lss = None
        if lss_config is not None:
            # Assert that the user context doesn't specify 'lss', which is
            # reserved for the large static store instance.
            assert 'lss' not in kwargs
            self.lss = large_static_store.get(lss_config)

        # Add any custom attributes.
        for k, v in kwargs.items():
            setattr(self, k, v)

    def raise_static_not_found(self, path):
        """Static file not found exception message helper.
        """
        msg = 'Static file not found'
        if self.lss is not None:
            msg += ' locally or in large static store'
        raise FileNotFoundError(f'{msg}: {path}')

    def static_last_modified(self, filename):
        """Return a datetime object representing the static file's
        last-modified time.
        """
        path = os.path.join(self.STATIC_DIR, filename)
        if os.path.exists(path):
            # The file exists locally, so stat it.
            last_modified = datetime.fromtimestamp(os.stat(path).st_mtime)
        elif self.lss and self.lss.exists(filename):
            # The file does not exist locally, so check the lss.
            last_modified = self.lss.meta(filename).last_modified
        else:
            self.raise_static_not_found(filename)
        # Truncate microseconds.
        return last_modified.replace(microsecond=0)

    def static(self, filename, raise_on_not_found=True):
        """Format filename as a static asset path, optionally assert that the
        file exists, and return the path. If file does not exist and
        raise_on_not_found=False, return None.
        """
        fs_path = f'{self.STATIC_DIR}/{filename}'
        # Check that file exists either locally or in the lss.
        if not os.path.isfile(fs_path):
            # If the file exist in the lss, return that URL.
            if not self.lss or not self.lss.exists(filename):
                if raise_on_not_found:
                    self.raise_static_not_found(fs_path)
                return None
            # File exists in lss.
            path = f'{self.large_static_store["endpoint"]}/{filename}'
        elif not self.is_large_static_storable(filename):
            # It's a small, local file.
            path = f'{self.SITE_RELATIVE_STATIC_DIR}/{filename}'
        else:
            # It's a large file.
            if self.production:
                path = f'{self.large_static_store["endpoint"]}/{filename}'
            else:
                # Warn if the file exists both locally and in the lss manifest.
                if self.lss and self.lss.exists(filename):
                    print(f'Large, local file "{filename}" exists in the LSS.')
                path = os.path.join(
                    self.SITE_RELATIVE_LARGE_STATIC_DIR,
                    filename
                )
        return path

    def is_large_static_storable(self, filename):
        """Return a bool indicating whether the specified file should be
        considered a large static asset that's subject to large static store
        offloading.
        """
        # Files in static subdirectories are excluded from consideration with
        # regard to large static store offloading, so if this file is in a
        # subdirectory, return False.
        if os.path.dirname(filename) != '':
            return False
        path = f'{self.STATIC_DIR}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')
        return os.stat(path).st_size / 1024 \
            >= self.STATIC_LARGE_FILE_THRESHOLD_KB

    def url(self, path):
        """Return path as an absolute URL.
        """
        return f'{self.base_url}/{path.lstrip("/")}'

    def static_url(self, filename):
        """Return an absolute URL for a static asset filename.
        """
        # Get the static path, which may be an absolute URL if environment is
        # production and asset qualifies for large storage.
        path = self.static(filename)
        if path.startswith(('http://', 'https://')):
            return path
        return self.url(path)

    def site_exists(self, filename):
        """Return a bool indicating whether filename exists in self.SITE_DIR.
        """
        return os.path.exists(os.path.join(self.SITE_DIR, filename))

    def site_open(self, path, mode, encoding=None):
        """Return a file handle for a path in self.SITE_DIR.
        """
        path = os.path.join(self.SITE_DIR, path.lstrip('/'))
        return open(path, mode, encoding=encoding)

###############################################################################
# Normalize Project Videos
###############################################################################

def add_source(context, video):
    """Add a VideoSource-type source property to the video dict that comprises
    a bunch of computed values.
    """
    filename = video['filename']
    video['source'] = VideoSource(
        filename=filename,
        mimetype=guess_mimetype(filename),
        url=context.static(filename),
        last_modified=context.static_last_modified(filename),
        poster_url=context.static(
            context.derivative_video_poster_filename_template.format(
                base_filename=os.path.splitext(filename)[0]
            )
        )
    )

def normalize_videos(context, videos):
    for video in videos:
        add_source(context, video)

###############################################################################
# Normalize Project Images
###############################################################################

def get_fallback_image_source(context, original_width, aspect, item_name,
                              asset_id):
    """Return a fallback image source tuple for the specified item name and
    # assset file number.
    """
    mimetype = context.prioritized_derivative_image_mimetypes[-1]
    width = min(original_width, context.fallback_image_width)
    height = width / aspect
    filename = context.derivative_image_filename_template.format(
        item_name=item_name,
        asset_id=asset_id,
        width=width,
        extension=guess_extension(mimetype)
    )
    url = context.static(filename)
    last_modified = context.static_last_modified(filename)
    return ImageSource(filename, mimetype, url, width, height, last_modified)

def add_sources(context, image):
    """Extend the image dict with a 'sources' property that comprises the available
    file sources as a dict in the format:
    'sources': {
      'original': <ImageSource>,
      'derivatives': [ ( <mimetype>, [ <ImageSource>, ... ] ), ... ],
      'fallback': <ImageSource>
    }
    """
    # Parse the filename.
    filename = image['filename']
    match = context.normalized_image_filename_regex.match(filename)
    item_name = match.group('item_name')
    asset_id = match.group('asset_id')
    original_width = int(match.group('width'))
    original_height = int(match.group('height'))
    aspect = original_height / original_width

    sources = {
        'original': ImageSource(
            filename,
            guess_mimetype(filename),
            context.static(filename),
            original_width,
            original_height,
            context.static_last_modified(filename)
        ),
        'derivatives': [],
        'fallback': get_fallback_image_source(
            context, original_width, aspect, item_name, asset_id
        )
    }

    # Sort widths descending.
    widths = sorted(context.derivative_image_widths, reverse=True)

    # If any widths are larger than the original image, add the original width
    # to the list and drop the larger values.
    i = next(i for i, width in enumerate(widths) if width < original_width)
    if i > 0:
        widths = [original_width] + widths[i:]

    # Add the derivative sources.
    for mimetype in context.prioritized_derivative_image_mimetypes:
        mimetype_derivative_sources = []
        for width in widths:
            # Generate the corresponding derivative filename.
            derivative_fn = context.derivative_image_filename_template.format(
                item_name=item_name,
                asset_id=asset_id,
                width=width,
                extension=guess_extension(mimetype)
            )
            url = context.static(derivative_fn, False)
            if url is not None:
                mimetype_derivative_sources.append(
                    ImageSource(
                        derivative_fn,
                        mimetype,
                        url,
                        width,
                        width / aspect,
                        context.static_last_modified(derivative_fn)
                    )
                )

        # Raise an exception if no derivative images were found.
        # Note that derivative at some widths may be missing
        # on account of the original image being smaller than that
        # width.
        if not mimetype_derivative_sources:
            raise AssertionError(
                f'No derivatives of type {mimetype} found for file:'\
                f'{image["filename"]}'
            )
        sources['derivatives'].append((mimetype, mimetype_derivative_sources))

    image['sources'] = sources

def normalize_images(context, images):
    for image in images:
        add_sources(context, image)

###############################################################################
# Context Normalization Helpers
###############################################################################

def normalize_projects(context, projects, all_tags):
    """Do an in-place normalization of the projects dict.
    """
    # Create a <project-name> -> <project-copy> map.
    name_project_map = {x['name']: x for x in projects}

    # Keep track of any invalid tags (i.e. not in all_tags) or types (i.e. not
    # a schema.org type name).
    invalid_d = {
        'tags': set(),
        'types': set(),
        'props': set(),
    }

    microdata_type_urls = set(microdata.Types.__dict__.values())
    microdata_props = set(microdata.Props.__dict__.values())

    for name, project in name_project_map.items():
        # Collect any invalid tags.
        invalid_d['tags'].update(set(project['tags']).difference(all_tags))

        # Normalize images.
        images = project.get('images')
        if images:
            normalize_images(context, images)

        # Normalize videos.
        videos = project.get('videos')
        if videos:
            normalize_videos(context, videos)

        # Expand project type name to full schema.org URL or collect it as
        # invalid.
        type_url = get_type_url(project['type'])
        if type_url in microdata_type_urls:
            project['type'] = type_url
        else:
            invalid_d['types'].add(project['type'])

        # Expand external_link_prop_type_name_urltype_url_tuples type names to
        # to full schema.org values and collect any invalid props, types, and
        # urltypes.
        for x in project.get(
                'external_link_prop_type_name_urltype_url_tuples', ()):
            prop, type, _, urltype, _ = x
            if prop is not None and prop not in microdata_props:
                invalid_d['props'].add(prop)
            if type is not None:
                if hasattr(microdata.Types, type):
                    x[1] = getattr(microdata.Types, type)
                else:
                    invalid_d['types'].add(type)
            if urltype not in microdata_props:
                invalid_d['props'].add(urltype)

        # Add any missing dependency properties.
        for k in (DEPENDS_ON, DEPENDENT_OF):
            if k not in project:
                continue
            other_k = DEPENDENT_OF if k == DEPENDS_ON else DEPENDS_ON
            for other_name in project[k]:
                other_project = name_project_map[other_name]
                # Do not add a dependent_of relationship for values that
                # already exist in collateral_creations.
                if (COLLATERAL_CREATIONS in other_project
                    and k == DEPENDENT_OF
                    and name in other_project[COLLATERAL_CREATIONS]):
                    continue
                if other_k in other_project:
                    if name not in other_project[other_k]:
                        other_project[other_k].append(name)
                else:
                    other_project[other_k] = [name]
    # Abort if any project specifies an invalid field value.
    error_strs = [
        f'invalid {k}: {list(v)}' for k, v in invalid_d.items() if v
    ]
    if error_strs:
        raise InvalidContext(', '.join(error_strs))

def normalize_context(context):
    """Do an in-place normalization of the context object, grooming values,
    adding defaults for unspecified fields, enriching with inferred data, etc.
    """
    # Strip any trailing base_url slash.
    context.base_url = context.base_url.rstrip('/')

    # Assert that all_tags is specified.
    all_tags = set(getattr(context, 'all_tags', ()))
    if not all_tags:
        raise InvalidContext('context must define an all_tags array that '\
                             'comprises the superset of all referenced tags.')

    # Compile regexes.
    context.normalized_image_filename_regex = re.compile(
        context.normalized_image_filename_regex
    )

    normalize_projects(context, context.projects, all_tags)
