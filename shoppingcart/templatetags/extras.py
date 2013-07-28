from django import template

register = template.Library()

@register.inclusion_tag('_ordertable.html')
def show_order(order):
    return {'order': order}