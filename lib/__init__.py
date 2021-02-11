"""General, Python2.7-friendly, utilities.
"""

import mimetypes
import os
import shutil
import re
from itertools import chain

SLUGIFY_REGEX = re.compile(r'[^\w]')

# Some toolz-type, functional helpers.
pluck = lambda key, dicts: [d[key] for d in dicts]
flatten = lambda iterable: chain(*iterable)

# Replace non-alpha chars with a hyphen and lowercase.
slugify = lambda s: SLUGIFY_REGEX.sub('-', s).lower()

def assert_ctx(context, k):
    if not hasattr(context, k):
        raise AssertionError('context has no attribute "{}"'.format(k))
    if not getattr(context, k):
        raise AssertionError(
            'context.{} is not defined, or otherwise falsy'.format(k)
        )
    return True

# Define am empty include/macro Head/Body placeholder function.
NotDefined = lambda context: ()

def copy_if_newer(src, dest):
    """Copy src to dest if src is newer and return a bool indicating whether
    the copy took place.
    """
    if (not os.path.exists(dest)
        or os.stat(src).st_mtime > os.stat(dest).st_mtime):
        shutil.copy2(src, dest)
        return True
    return False

def guess_mimetype(path):
    """Define a mimetypes.guess_type() wrapper that returns just the type and
    also handles webp.
    """
    if path.endswith('.webp'):
        return 'image/webp'
    return mimetypes.guess_type(path)[0]

def guess_extension(mimetype):
    """Define a mimetypes.guess_extension() wrapper that handles webp and
    raises an exception on unguessable type.
    """
    if mimetype == 'image/webp':
        return '.webp'
    extension = mimetypes.guess_extension(mimetype)
    if extension is None:
        raise AssertionError(
            'can not guess extension for mimetype: {}'.format(mimetype)
        )
    return extension

def listfiles(_dir):
    """Yield each non-directory entry in a directory along with its full path.
    """
    for filename in os.listdir(_dir):
        path = os.path.join(_dir, filename)
        if not os.path.isdir(path):
            yield filename, path
