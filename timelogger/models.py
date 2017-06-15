# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User_accounts(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name

    def to_object(self):
        response = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "password": self.password,
            "created_date": self.created_date.strftime("%m/%d/%Y"),
            "updated_date": self.updated_date.strftime("%m/%d/%Y"),
        }
        return response

