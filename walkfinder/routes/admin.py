from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Mapgens, Start

# Register your models here.
admin.site.register(Start)

@admin.register(Mapgens)
class MapgensAdmin(OSMGeoAdmin):
    list_display = ('home_loc', 'target_time', 'speed_mph')
