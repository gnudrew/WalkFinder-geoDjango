# Generated by Django 3.2 on 2021-05-13 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='start',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=44.787221, max_digits=9),
        ),
        migrations.AddField(
            model_name='start',
            name='lon',
            field=models.DecimalField(decimal_places=6, default=-93.146939, max_digits=9),
        ),
        migrations.AddField(
            model_name='start',
            name='target_time',
            field=models.IntegerField(default=15),
        ),
    ]
