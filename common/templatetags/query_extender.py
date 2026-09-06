import urllib.parse
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_param_add(context, key, value):
    dict_: dict = context["request"].GET.copy() # GET is read only, so we copy it to be able to manipulate it
    dict_[key] = value
    return "?" + urllib.parse.urlencode(dict_)
    #{"name": "sasho", "page": 10} -> ?name=sasho&page=10