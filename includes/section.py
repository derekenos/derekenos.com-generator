
from lib import NotDefined
from lib.htmlephant import (
    Div,
    H1,
    H2,
)

Head = NotDefined

def Body(context, title, subtitle=None, children=()):
    wrapper = Div(_class='section', children=[H1(title)])
    if subtitle:
        wrapper.children.append(H2(subtitle))
    wrapper.children.extend(children)
    return (wrapper,)
