"""General, Python2.7-friendly, utilities.
"""

import hashlib
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
    # Reutrn '.jpg' for image/jpeg. Python < 3.7 returns '.jpe'.
    if mimetype == 'image/jpeg':
        return '.jpg'
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

def md5sum(path):
    """Return the MD5 hash of the file contents.
    """
    BUF_SIZE = 1024 * 64
    buf = bytearray(BUF_SIZE)
    mv = memoryview(buf)
    md5 = hashlib.md5()
    with open(path, 'rb') as fh:
        while True:
            num_bytes = fh.readinto(buf)
            md5.update(mv[:num_bytes])
            if num_bytes < BUF_SIZE:
                break
    return md5.hexdigest()
