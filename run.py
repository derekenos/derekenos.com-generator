
import os

from lib.htmlephant import Document

import includes.head
import includes.body

PAGES_DIR = 'pages'
SITE_DIR = 'site'

_open = lambda path: open(os.path.join(SITE_DIR, path), 'w', encoding='utf-8')

if __name__ == '__main__':
    # Build the global context dict.
    context = {
        'page_names': [
            mod_name.rsplit('.', 1)[0]
            for mod_name in os.listdir(PAGES_DIR)
            if mod_name.endswith('.py')
        ],
        'current_page': None,
    }

    for page_name in context['page_names']:
        context['current_page'] = page_name
        with _open(f'{page_name}.html') as fh:
            mod = __import__(f'{PAGES_DIR}.{page_name}', fromlist=page_name)
            # Include the global head elements.
            head_els = includes.head.Head(context) + mod.Head(context)
            body_els = includes.body.Body(context) + mod.Body(context)
            doc = Document(body_els, head_els)
            for c in doc:
                fh.write(c)
