import bleach
import markdown
from bleach import DEFAULT_CALLBACKS
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'br',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'p',
    'table',
    'tbody',
    'thead',
    'tr',
    'td',
    'th',
    'div',
    'span',
    'hr',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'pre',
    # Update doc/user/markdown.rst if you change this!
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'class'],
    'abbr': ['title'],
    'acronym': ['title'],
    'table': ['width'],
    'td': ['width', 'align'],
    'div': ['class'],
    'p': ['class'],
    'span': ['class', 'title'],
    # Update doc/user/markdown.rst if you change this!
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto', 'tel']


def markdown_compile_email(source):
    return bleach.linkify(bleach.clean(
        markdown.markdown(
            source,
            extensions=[
                'markdown.extensions.sane_lists',
                #  'markdown.extensions.nl2br' # disabled for backwards-compatibility
            ]
        ),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
    ), parse_email=True)


def markdown_compile(source):
    return bleach.clean(
        markdown.markdown(
            source,
            extensions=[
                'markdown.extensions.sane_lists',
                'markdown.extensions.nl2br'
            ]
        ),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
    )


@register.filter
def rich_text(text: str, **kwargs):
    """
    Processes markdown and cleans HTML in a text input.
    """
    text = str(text)
    body_md = bleach.linkify(
        markdown_compile(text),
        callbacks=DEFAULT_CALLBACKS,
        parse_email=True
    )
    return mark_safe(body_md)