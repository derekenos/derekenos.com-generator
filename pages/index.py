
from itertools import chain

from lib.htmlephant import (
    Div,
    H1,
    Title,
)

from includes import project_card
from includes import collection

Head = lambda context: (
    Title('Derek Enos | Projects'),
)

Body = lambda context: (
    Div(
        _class='content projects',
        children=(
            H1('Selected projects'),
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
