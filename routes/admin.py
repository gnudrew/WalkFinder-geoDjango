from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Mapgens 

# Register your models here.
@admin.register(Mapgens)
class MapgensAdmin(OSMGeoAdmin):
    list_display = ('home_loc', 'target_time', 'speed_mph')
