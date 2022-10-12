from urllib.parse import quote, urljoin
from django.templatetags.static import PrefixNode
from django import template

register = template.Library()


@register.simple_tag
def media(path):
    """
    Given a relative path to a static asset, return the absolute path to the
    asset.
    """
    return urljoin(PrefixNode.handle_simple("MEDIA_URL"), quote(str(path)))
