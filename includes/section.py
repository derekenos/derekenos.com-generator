
from lib import NotDefined
from lib.htmlephant import (
    H2,
    H3,
    Section,
)

Head = NotDefined

def Body(context, title=None, subtitle=None, children=(), **attrs):
    section = Section(**attrs)
    if title:
        section.children.append(H2(title))
    if subtitle:
        section.children.append(H3(subtitle))
    section.children.extend(children)
    return (section,)
