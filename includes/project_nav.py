
from lib import (
    NotDefined,
    stubify,
)
from lib.htmlephant import (
    Anchor,
    Div,
    Span,
    Style,
)

Head = lambda context: (
    Style(
"""

#project-nav-outer {
  padding: 0;
  white-space: nowrap;
}

#project-nav-inner {
  overflow-x: scroll;
  scrollbar-width: thin;
}

.project-nav-link {
  display: inline-block;
  white-space: norwap;
  padding: 1.4rem;
  text-decoration: none;
}

.project-nav-link:nth-child(even) {
  background-color: rgba(0, 0, 0, 0.2);
}

.project-nav-link.current {

}

"""
    ),
)

def Body(context, current_project):
    outer = Div(id='project-nav-outer')
    inner = Div(id='project-nav-inner')
    outer.children.append(inner)
    for project in sorted(context.projects,
                          key=lambda x: x['name'] == current_project['name'],
                          reverse=True):
        if project['name'] == current_project['name']:
            inner.children.append(
                Span(
                    project['name'],
                    _class='project-nav-link current'
                )
            )
        else:
            inner.children.append(
                Anchor(
                    project['name'],
                    _class='project-nav-link',
                    href=f'project-{stubify(project["name"])}.html'
                )
            )
    return (outer,)
