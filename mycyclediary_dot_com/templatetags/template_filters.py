from django import template
from stravalib import unithelper
from units import unit

register = template.Library()

@register.filter
def meters_to_miles(value):
    return unithelper.miles(unit('m')(value))

@register.filter
def seconds_to_hours(value):
    return unithelper.hours(unit('s')(value))
