from django import template
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter
def duration(td):

    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f'{days} days ' if days else ''
    hours_str = f'{hours} hours ' if hours else ''
    minutes_str = f'{minutes}m ' if minutes else ''
    seconds_str = f'{seconds}s' if seconds and not hours_str else ''

    return f'{days_str}{hours_str}{minutes_str}{seconds_str}'

@register.simple_tag(takes_context=True)
def clean_url(context):
    request = context['request']
    return request.build_absolute_uri(request.path)

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None

@register.filter
def module_name(things, category):
    return things.filter(category=category)

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
