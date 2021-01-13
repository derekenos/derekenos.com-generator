
from lib.htmlephant_extensions import Em
from lib.htmlephant import (
    H3,
    Paragraph,
)

from includes import section

Head = lambda context: ()

Body = lambda context: (
    Paragraph('These are things that I have considered making or doing.'),
    *section.Body(
        context,
        'Initiatives',
        'borad efforts',
        children=(
            H3('Teaching Arcade'),
            Paragraph(
                """Arcade games are an exciting and well-loved manifestation of physical computing, but in constrast to peoples' burgeoning ability to author game software, creating new, exciting, and specific physical interfaces through which to interact with these games remains largely out of reach. This initiative would create a space to teach physical interface design, programming, and fabrication in conjunction with game software design and programming, with the end goal of creating a physical gaming appliance to be presented in an arcade gallery and/or duplicated for sale. Game design instruction will focus on leveraging modern web technologies (e.g. HTML5, Javascript, Web Components) and development practices (e.g. testing, version control) to maximize the potential of applying what is learned in a professional capacity. Hardware design instruction will focus on leveraging modern, inexpensive, commodity components and modular construction practices."""
            )
        )
    )
)
