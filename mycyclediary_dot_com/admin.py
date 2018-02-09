from django.contrib import admin
from .models import *

admin.site.register(Athlete)

@admin.register(Gear, Bike, Shoe, Component)
class GearAdmin(admin.ModelAdmin):
    list_display = ('name','athlete')

@admin.register(ComponentComponent)
class BikeComponentAdmin(admin.ModelAdmin):
    list_display = ('athlete','component','parent_component')
