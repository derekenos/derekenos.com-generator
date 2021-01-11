
from lib import assert_ctx
from lib.htmlephant import Script

Head = lambda context: assert_ctx(context, 'google_analytics_id') and (
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
