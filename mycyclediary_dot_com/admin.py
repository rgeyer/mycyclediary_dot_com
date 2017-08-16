from django.contrib import admin
from .models import *

admin.site.register(athlete)

@admin.register(gear, bike, shoe, component)
class GearAdmin(admin.ModelAdmin):
    list_display = ('name','athlete')

@admin.register(component_component)
class BikeComponentAdmin(admin.ModelAdmin):
    list_display = ('athlete','component','parent_component')
