from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Mapgens 

# Register your models here.

@admin.register(Mapgens)
class MapgensAdmin(OSMGeoAdmin):
    list_display = ('created_at','home_loc',('target_time','dist')) # diplsayed in summary page
    fields = ('created_at','home_loc',('target_time','dist')) # displayed in object detail page
    readonly_fields = ('created_at',) # cause this field to be displayed (otherwise hidden)
