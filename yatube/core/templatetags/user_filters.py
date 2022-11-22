import json

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def add_id(field, css):
    return field.as_widget(attrs={'id': css})


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
