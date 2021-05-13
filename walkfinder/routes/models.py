from django.db import models

class Start(models.Model):
    target_time = models.IntegerField(default=15)
    lat = models.DecimalField(decimal_places=6, max_digits=9, default=44.787221)
    lon = models.DecimalField(decimal_places=6, max_digits=9, default=-93.146939)