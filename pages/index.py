
from lib.htmlephant import (
    Div,
    Title,
)

from includes import project_card

Head = lambda context: (
    Title('Projects'),
)

Body = lambda context: (
    Div(
        _class="content",
        children=[
            Div(_class='item', children=project_card.Body(context, **prj))
            for prj in context.projects
        ]
    ),
)
