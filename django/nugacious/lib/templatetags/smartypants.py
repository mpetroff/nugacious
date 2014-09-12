from django import template
from django.template.defaultfilters import stringfilter
import smartypants

register = template.Library()

@register.filter(name='smartypants', is_safe=True)
@stringfilter
def smartypants_filter(text):
    return smartypants.smartypants(text)
