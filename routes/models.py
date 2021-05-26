from django.contrib.gis.db import models

class Start(models.Model):
# this is a test Model
    target_time  = models.IntegerField(default=15)
    lat          = models.DecimalField(decimal_places=6, max_digits=9, default=44.786761)
    lon          = models.DecimalField(decimal_places=6, max_digits=9, default=-93.145689)
    # 44.786761, -93.145689 <-- Lebanon Hills path intersection

class Mapgens(models.Model):
# this table holds data to (re)generate graph objects + map
    home_loc     = models.PointField() # (lat,lon) at home marker
    start_loc    = models.PointField() # (lat,lon) at route start node
    end_loc      = models.PointField(null=True) # (lat,lon) at route end node
    target_time  = models.IntegerField() # minutes
    speed_mph    = models.DecimalField(decimal_places=1, max_digits=3) # miles per hour, e.g. 3.1mph
    speed_mpm    = models.DecimalField(decimal_places=1, max_digits=5) # meters per minute
    dist         = models.DecimalField(decimal_places=0, max_digits=6) # input for ox.graph...
    dist_type    = models.CharField(max_length=20) # input for ox.graph... e.g. 'network'
    network_type = models.CharField(max_length=20) # input for ox.graph... e.g. 'walk'
    # route_ids    = models.IntegerField() # match to Routes objects generated from this

class Routes(models.Model):
# this table holds route data
    # graph        = models.?
    # node_list    = models.JSONField
    pass

class Walks(models.Model):
# this table holds data from hot location walk
    pass
