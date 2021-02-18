
from lib.htmlephant import Script

Head = lambda context: (
    Script(
        _async='',
        src=f'https://www.googletagmanager.com/gtag/js?id={context.google_analytics_id}'
    ),
    Script(
f"""
window.dataLayer = window.dataLayer || [];
function gtag() {{
  dataLayer.push(arguments);
}}
gtag('js', new Date());
gtag('config', '{context.google_analytics_id}');
"""
    )
)


Body = lambda context: ()
