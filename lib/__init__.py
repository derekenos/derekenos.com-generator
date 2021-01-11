
def assert_ctx(context, k):
    if not hasattr(context, k):
        raise AssertionError(f'context has no attribute "{k}"')
    if not getattr(context, k):
        raise AssertionError(f'context.{k} is not defined, or otherwise falsy')
    return True
