"""Microdata constants.
"""
from types import SimpleNamespace


Types = SimpleNamespace(**{
    k: f'https://schema.org/{k}'
    for k in (
            'Collection',
            'ContactPoint',
            'CreativeWork',
            'ImageObject',
            'Intangible',
            'MediaObject',
            'Organization',
            'Person',
            'SoftwareApplication',
            'SoftwareSourceCode',
            'VideoObject',
    )
})

Props = SimpleNamespace(**{
    k: k for k in (
        'abstract',
        'applicationCategory',
        'associatedMedia',
        'codeRepository',
        'contactPoint',
        'contentUrl',
        'description',
        'email',
        'encodingFormat',
        'hasPart',
        'image',
        'installUrl',
        'isPartOf',
        "mainEntityOfPage",
        'name',
        'operatingSystem',
        'position',
        'sameAs',
        'subjectOf',
        'thumbnailUrl',
        'uploadDate',
        'url',
    )
})
