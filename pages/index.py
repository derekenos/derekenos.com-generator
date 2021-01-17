
from lib.htmlephant_extensions import (
    OGMeta,
    StdMeta,
)
from lib.htmlephant import (
    Div,
    H1,
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
                [
                    project_card.Body(context, **prj)
                    for prj in context.projects
                    if not prj.get('hide_card', False)
                ]
            )
        )
    ),
)
