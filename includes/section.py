
from lib import NotDefined
from lib.htmlephant_extensions import Section
from lib.htmlephant import (
    H2,
    H3,
)

Head = NotDefined

def Body(context, title, subtitle=None, children=()):
    section = Section(children=[H2(title)])
    if subtitle:
        section.children.append(H3(subtitle))
    section.children.extend(children)
    return (section,)
