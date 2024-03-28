from django import template
from django.utils.translation import activate, gettext as _
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()

@register.filter
def persian_timesince(value):
    now = timezone.now()
    delta = now - value

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    time_str = ""
    if days > 0:
        time_str += f"{days} روز، "
    if hours > 0:
        time_str += f"{hours} ساعت، "
    if minutes > 0 or (days == 0 and hours == 0):
        time_str += f"{minutes} دقیقه، "

    activate('fa')
    return '{} پیش'.format(time_str.rstrip("، "))
