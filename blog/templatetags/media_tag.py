from django import template
from config.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def mediapath(value):
    return MEDIA_URL + str(value)
