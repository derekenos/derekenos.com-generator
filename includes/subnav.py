
from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Li,
    Nav,
    Ol,
    Script,
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

# Return a sub-navigation, assuming that the first name/url pair is the
# currently active item.
Body = lambda context, name_url_pairs, active_name: (
    Nav(
        id='sub-nav',
        _aria_labelledby="active-main-nav-tab",
        children=(
            Ol(
                children = [
                    Li(name, _class='active')
                    if name == active_name else Li(
                            children=(
                                Anchor(name, href=url),
                            )
                    )
                    for name, url in name_url_pairs
                ]
            ),
        )
    ),
)
