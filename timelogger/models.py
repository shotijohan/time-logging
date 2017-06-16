# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TimeInTimeOut(models.Model):
    user = models.ForeignKey(User)
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True)
    duration = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id) + \
               "(" + self.time_in.strftime("%H:%M:%S") + \
               "-" + (self.time_out.strftime("%H:%M:%S") if self.time_out else "In Progress") +\
               ") total_hours:" + str(self.duration if self.duration else "")
