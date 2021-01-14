
from lib import NotDefined
from lib.htmlephant_extensions import Section
from lib.htmlephant import (
    H1,
    H2,
)

Head = NotDefined

def Body(context, title, subtitle=None, children=()):
    section = Section(children=[H1(title)])
    if subtitle:
        section.children.append(H2(subtitle))
    section.children.extend(children)
    return (section,)
