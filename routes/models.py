from django.contrib.gis.db import models

# 44.78676, -93.14569 <-- Lebanon Hills Regional Park, 5-way path intersection

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        abstract = True

class Mapgens(TimeStampMixin):
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

class Walks(TimeStampMixin):
# this table holds data from hot location walk
    pass
