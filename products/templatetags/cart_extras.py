from django import template

register = template.Library()


@register.filter
def multiply(a, b):
    return a * b


@register.filter
def cart_total(items):
    return sum(item.quantity * item.product.price for item in items)
