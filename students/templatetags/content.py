from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
