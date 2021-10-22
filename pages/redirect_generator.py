
import includes.redirect

from lib.htmlephant import (
    Meta,
    OGMeta,
    StdMeta,
    Title,
)

FILENAME_GENERATOR = lambda redirect: f'{redirect["slug"]}.html'

CONTEXT_ITEMS_GETTER = lambda context: context.redirects

Head = lambda context: includes.redirect.Head(
    context,
    (item:=context.generator_item)['destination'],
    item['slug'],
    item.get('description')
)

Body = lambda context: ()
