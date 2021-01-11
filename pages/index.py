
from lib.htmlephant import (
    Div,
    Title,
)

from includes import project

Head = lambda context: (
    Title('Projects'),
)

Body = lambda context: (
    Div(
        _class='item',
        children=project.Body(
            context,
            name='Cardboard Boxcade',
            desc='Custom physical controls for browser-based HTML/Javascript '\
            'applications.',
            tags=('esp32', 'micropython', 'iot', 'videogame'),
            img_base_fn='cardboard_boxcade_thumb',
            img_alt='photo of a cardboard box with a screen and switches'
        )
    ),
)
