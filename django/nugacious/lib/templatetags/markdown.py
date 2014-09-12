from django import template
from django.template.defaultfilters import stringfilter
import markdown

register = template.Library()

@register.filter(name='markdown', is_safe=True)
@stringfilter
def markdown_filter(text):
    return markdown.markdown(text)
