from lib.htmlephant_extensions import Main
from lib import (
    flatten,
    pluck,
)
from lib.htmlephant import (
    Anchor,
    H1,
    Link,
    OGMeta,
    Paragraph,
    Span,
    StdMeta,
    Title,
)

from includes import (
    collection,
    project_card,
    section,
)

DESCRIPTION = "Home page displaying selected projects"

Head = lambda context: (
    StdMeta("description", DESCRIPTION),
    OGMeta("description", DESCRIPTION),
    StdMeta(
        "keywords", ",".join(sorted(set(flatten(pluck("tags", context.projects)))))
    ),
    Title(f"{context.name} | Home"),
    # Support http://microformats.org/wiki/RelMeAuth
    *[Link(rel="me", href=url) for _, url in context.social_name_url_pairs],
)

Body = lambda context: (
    Main(
        _class="home",
        children=(
            H1(DESCRIPTION),
            *section.Body(
                context,
                children=[
                    Paragraph(id="topline", children=[
                        Span("I'm working to build our local capacity to design and produce more of the things that we want and need, here in Beacon, New York."),
                        Anchor("Get in touch", href="/about"),
                        Span("if you're interested in the same."),
                    ]),
                    *collection.Body(
                        context,
                        name="Selected Projects",
                        items=[
                            project_card.Body(context, **prj)
                            for prj in context.projects
                            if not prj.get("hide_card", False)
                        ],
                    ),
                ],
            ),
        ),
    ),
)
