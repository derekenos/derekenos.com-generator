
from lib.htmlephant import Script

ID = 'UA-19335494-1'

Head = lambda context: (
    Script(
        _async='',
        src=f'https://www.googletagmanager.com/gtag/js?id={ID}'
    ),
    Script(
f"""
window.dataLayer = window.dataLayer || [];
function gtag() {{
  dataLayer.push(arguments);
}}
gtag('js', new Date());
gtag('config', '{ID}');
"""
    )
)


Body = lambda context: ()
