# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timelogger.models import TimeInTimeOut
from timelogger.models import UserProfile
from django.contrib import admin

# Register your models here.
admin.site.register(TimeInTimeOut)
admin.site.register(UserProfile)