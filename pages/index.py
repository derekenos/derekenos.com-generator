
from lib import microdata as md
from lib.htmlephant import (
    Div,
    H1,
    OGMeta,
    StdMeta,
    Title,
)

from includes import project_card
from includes import collection

DESCRIPTION = 'Home page displaying selected projects'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | Projects'),
)

Body = lambda context: (
    Div(
        _class='content projects',
        children=(
            H1(DESCRIPTION),
            *collection.Body(
                context,
                name='Selected Projects',
                items=[
                    project_card.Body(context, **prj)
                    for prj in context.projects
                    if not prj.get('hide_card', False)
                ]
            )
        )
    ),
)
