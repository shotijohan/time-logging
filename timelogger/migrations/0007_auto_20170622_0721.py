# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('timelogger', '0006_auto_20170621_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeintimeout',
            name='description',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='timeintimeout',
            name='time_in',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timeintimeout',
            name='time_out',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timeintimeout',
            name='user',
            field=models.ForeignKey(related_name='timeintimeout', to=settings.AUTH_USER_MODEL),
        ),
    ]
