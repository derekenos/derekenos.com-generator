
from lib import NotDefined
from lib.htmlephant import (
    H1,
    H2,
)

Head = NotDefined

def Body(context, title, subtitle=None, children=()):
    if subtitle:
        return H1(title), H2(subtitle), *children
    return H1(title), *children
