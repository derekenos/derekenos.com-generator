
import os
from datetime import datetime

from lib import large_static_store

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
    SITE_RELATIVE_LARGE_STATIC_DIR = f'static/large'
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
        # Add any custom attributes.
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Maybe instantiate a large static store.
        assert not hasattr(self, 'lss')
        self.lss = None
        if self.large_static_store is not None:
            self.lss = large_static_store.get(self.large_static_store)

    def static_last_modified_iso8601(self, filename):
        return datetime.fromtimestamp(
            os.stat(os.path.join(self.STATIC_DIR, filename)).st_mtime
        ).isoformat()

    def static(self, filename):
        """Format filename as a static asset path, assert that the file exists,
        and return the path.
        """
        fs_path = f'{self.STATIC_DIR}/{filename}'
        # Check that file exists either locally or in the lss.
        if not os.path.isfile(fs_path):
            # If the file exist in the lss, return that URL.
            if not hasattr(self, 'lss') or not self.lss.exists(filename):
                raise AssertionError(f'Path is not a regular file: {fs_path}')
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
                if hasattr(self, 'lss') and self.lss.exists(filename):
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
