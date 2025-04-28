
from lib import NotDefined
from lib.htmlephant import (
    NOEL,
    Anchor,
    Br,
    Img,
    Li,
    Nav,
    Ol,
    Script,
    Span,
)

Head = lambda context: (
    Script(
"""
document.addEventListener("DOMContentLoaded", () => {
  // Scroll sub-nav to the current active tab.
  const subnavOl = document.querySelector("#sub-nav > ol")
  const activeLi = subnavOl.querySelector("li.active")
  subnavOl.scrollLeft = activeLi.offsetLeft
})
"""
    ),
)

ThumbEls = lambda image: (
    Img(
        src=image['sources']['derivatives'][-1][1][-1].url,
        alt=image['name']
    ),
    Br()
) if image is not None else ()

ActiveLi = lambda name, image: Li(_class='active', children=(
    *ThumbEls(image),
    Span(name)
))

InactiveLi = lambda name, image, url: Li(children=(
    Anchor(href=url, children=(
        *ThumbEls(image),
        Span(name)
    )),
))

# Return a sub-navigation, assuming that the first name/url pair is the
# currently active item.
Body = lambda context, name_url_image_tuples, active_name: (
    Nav(
        id='sub-nav',
        _aria_labelledby="active-main-nav-tab",
        children=(
            Ol(
                children = [
                    ActiveLi(name, image) if name == active_name
                    else InactiveLi(name, image, url)
                    for name, url, image in name_url_image_tuples
                ]
            ),
        )
    ),
)
