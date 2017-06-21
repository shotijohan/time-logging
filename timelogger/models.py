# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TimeInTimeOut(models.Model):
    user = models.ForeignKey(User)
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True)
    duration = models.FloatField(default=0.0)
    description = models.CharField(max_length=500, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "id:" + str(self.id) + (self.user.last_name.title() + "," if self.user.last_name else "") + " " + \
               (self.user.first_name.title() if self.user.first_name else self.user.username.title()) + \
               " (" + self.time_in.strftime("%H:%M:%S") + \
               "-" + (self.time_out.strftime("%H:%M:%S") if self.time_out else "In Progress") + \
               ") total_hours:" + str(self.duration if self.duration else "")

    def to_object(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "first_name": self.user.first_name.title() if self.user.first_name else "",
            "last_name": self.user.last_name.title() if self.user.last_name else "",
            "time_in": self.time_in.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone("Asia/Manila")).strftime("%m/%d/%Y %H:%M") if self.time_in else None,
            "time_out": self.time_out.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone("Asia/Manila")).strftime("%m/%d/%Y %H:%M") if self.time_out else None,
            "duration": abs(round(self.duration, 2)) if self.duration else 0,
            "description": self.description,
            "unrounded_of_duration": self.duration if self.duration else 0,
            "created_date": self.created_date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Manila")).strftime("%m/%d/%Y %H:%M")
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    hipchat_send_notification_token = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user.id) + " " + \
               self.user.last_name + "," + \
               self.user.first_name + " (hipchat:" + \
               self.hipchat_send_notification_token + ")"

    def to_object(self):
        return {
            "user": self.user,
            "user_id": self.user_id,
            "hipchat_token": self.hipchat_send_notification_token
        }