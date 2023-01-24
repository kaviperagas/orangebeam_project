import datetime
from django import template

register = template.Library()


@register.simple_tag
def plus_days(value, days):
    new_date = value + datetime.timedelta(days=days)
    return new_date
