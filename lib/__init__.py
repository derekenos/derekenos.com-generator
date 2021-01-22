
import os
import shutil
import re

SLUGIFY_REGEX = re.compile(r'[^\w]')

# Replace non-alpha chars with a hyphen and lowercase.
slugify = lambda s: SLUGIFY_REGEX.sub('-', s).lower()

def assert_ctx(context, k):
    if not hasattr(context, k):
        raise AssertionError(f'context has no attribute "{k}"')
    if not getattr(context, k):
        raise AssertionError(f'context.{k} is not defined, or otherwise falsy')
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
