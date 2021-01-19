
from lib import NotDefined
from lib.htmlephant import (
    H2,
    H3,
    Section,
)

Head = NotDefined

def Body(context, title, subtitle=None, children=(), **attrs):
    section = Section(children=[H2(title)], **attrs)
    if subtitle:
        section.children.append(H3(subtitle))
    section.children.extend(children)
    return (section,)
