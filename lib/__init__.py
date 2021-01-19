
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
