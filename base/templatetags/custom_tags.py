from django import template

register = template.Library()


@register.simple_tag
def date_variance(value1, value2):
    new_date = value1 - value2
    return new_date.days


@register.simple_tag
def days_variance(value1, value2):
    new_date = value1 - value2
    return new_date


@register.simple_tag
def percentage_variance(value1, value2):
    new_percentage = value1 - value2
    return new_percentage
