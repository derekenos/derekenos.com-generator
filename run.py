
import os

from lib.htmlephant import Document

PAGES_DIR = 'pages'
SITE_DIR = 'site'

_open = lambda path: open(os.path.join(SITE_DIR, path), 'w', encoding='utf-8')

if __name__ == '__main__':
    for mod_name in os.listdir(PAGES_DIR):
        if not mod_name.endswith('.py') or mod_name == '__init__.py':
            continue
        page_name = mod_name.rsplit('.', 1)[0]
        with _open(f'{page_name}.html') as fh:
            mod = __import__(f'{PAGES_DIR}.{page_name}', fromlist=page_name)
            doc = Document(mod.BODY_ELS, mod.HEAD_ELS)
            for c in doc:
                fh.write(c)
