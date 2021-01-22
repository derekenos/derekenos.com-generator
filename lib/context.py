
import os
from datetime import datetime

from lib import large_static_store

COLLATERAL_CREATIONS = 'collateral_creations'
DEPENDS_ON = 'depends_on'
DEPENDENT_OF = 'dependent_of'

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
    STATIC_LARGE_FILE_THRESHOLD_MB = 1
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

    def static_last_modified_iso8601(self, filename):
        # If the file exists, locally, stat it and return the result.
        path = os.path.join(self.STATIC_DIR, filename)
        if os.path.exists(path):
            return datetime.fromtimestamp(os.stat(path).st_mtime).isoformat()
        # The file does not exist locally, so check the lss.
        if self.lss and self.lss.exists(filename):
            return self.lss.meta(filename).last_modified.isoformat()
        self.raise_static_not_found(filename)

    def static(self, filename):
        """Format filename as a static asset path, assert that the file exists,
        and return the path.
        """
        fs_path = f'{self.STATIC_DIR}/{filename}'
        # Check that file exists either locally or in the lss.
        if not os.path.isfile(fs_path):
            # If the file exist in the lss, return that URL.
            if not self.lss or not self.lss.exists(filename):
                self.raise_static_not_found(fs_path)
            # File exists in lss.
            path = f'{self.large_static_store["endpoint"]}/{filename}'
        elif not self.is_large_static(filename):
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

    def is_large_static(self, filename):
        path = f'{self.STATIC_DIR}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')
        return os.stat(path).st_size / 1024 / 1024 \
            >= self.STATIC_LARGE_FILE_THRESHOLD_MB

    def url(self, path):
        """Return path as an absolute URL.
        """
        return f'{self.base_url if self.production else ""}/{path.lstrip("/")}'

    def static_url(self, filename):
        """Return an absolute URL for a static asset filename.
        """
        return self.url(self.static(filename))

    def open(self, path):
        """Return a writable UTF-8 file handle for a self.SITE_DIR sub-path.
        """
        path = os.path.join(self.SITE_DIR, path.lstrip('/'))
        return open(path, 'w', encoding='utf-8')

###############################################################################
# Context Normalization Helpers
###############################################################################

def normalize_projects(projects):
    """Do an in-place normalization of the projects dict.
    """
    # Create a <project-name> -> <project-copy> map.
    name_project_map = {x['name']: x for x in projects}

    # Add any missing dependency properties.
    for name, project in name_project_map.items():
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

def normalize_context(context):
    """Do an in-place normalization of the context object, grooming values,
    adding defaults for unspecified fields, enriching with inferred data, etc.
    """
    # Strip any trailing base_url slash.
    context.base_url = context.base_url.rstrip('/')

    normalize_projects(context.projects)
