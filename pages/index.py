
from lib.htmlephant import (
    Paragraph,
    Style,
    Title,
)

Head = lambda context: (
    Title('Projects'),
    Style('body { font-size: 2rem; }'),
)

Body = lambda context: (
    Paragraph('testing'),
)
