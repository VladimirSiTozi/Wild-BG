from django import template
import datetime

register = template.Library()

@register.filter
def format_duration(value):
    if not isinstance(value, datetime.timedelta):
        return value

    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} ч {minutes} мин"
