# Generated by Django 3.2.3 on 2021-05-19 07:44

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20210513_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapgens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_loc', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('start_loc', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('end_loc', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('target_time', models.IntegerField()),
                ('speed_mph', models.DecimalField(decimal_places=1, max_digits=3)),
                ('speed_mpm', models.DecimalField(decimal_places=1, max_digits=5)),
                ('dist', models.DecimalField(decimal_places=0, max_digits=6)),
                ('dist_type', models.CharField(max_length=20)),
                ('network_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Walks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
