# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from pprint import pprint

import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views.generic import View
import pytz
from timelogger.models import TimeInTimeOut
from .constants import *


# Create your views here.
def to_hours(seconds_var):
    return float(seconds_var / 3600)


def render_json(response_data):
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class Login(View):

    def get(self, request):
        if request.user.is_authenticated():
            jinja_data = {}
            time = TimeInTimeOut.objects
            time = time.filter(user=request.user)
            time = time.filter(duration=0.0)

            if time:
                jinja_data['status'] = "in progress"
                jinja_data['time'] = time[0]
            jinja_data['user'] = request.user
            return render(request, 'timelogger/home.html', jinja_data)
        return render(request, 'timelogger/login.html')

    def post(self, request):
        post_data = request.POST
        if post_data:
            user = authenticate(
                username=post_data.get("username"),
                password=post_data.get("password")
            )
            if user:
                login(request, user)
                return redirect("/")
            else:
                return render(request, 'timelogger/login.html', {"message" : INVALID_CREDENTIALS})


class Register(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/')
        return render(request, 'timelogger/register.html')

    def post(self, request):
        post_data = request.POST
        if post_data:
            User.objects.create_user(
                username=post_data.get('username'),
                email=post_data.get('email'),
                first_name=post_data.get('first_name'),
                last_name=post_data.get('last_name'),
                password=post_data.get('password'),
            )
            user_auth = authenticate(
                username=post_data.get('username'),
                password=post_data.get('password')
            )
            if user_auth:
                login(request, user_auth)
                return redirect("/")
            else:
                return HttpResponse("ERROR OCCURRED! :(")


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect("/")


class TimeInTimeOutHandler(View):

    def post(self, request):
        if request.user.is_authenticated():
            if request.POST['action'] == "time-in":
                time = TimeInTimeOut()
                time.user = request.user
                time.time_in = datetime.utcnow().replace(tzinfo=pytz.utc)
                time.save()
                response_data = {
                    "message": "OK!",
                    "time_id": str(time.id),
                    "action": "time-out"
                }
                return render_json(response_data)

            elif request.POST['action'] == "time-out":
                time_id = request.POST['time_id']
                if time_id:
                    time = TimeInTimeOut.objects.get(id=time_id)
                    if time:
                        time.time_out = datetime.utcnow().replace(tzinfo=pytz.utc)
                        time_diff = time.time_out - time.time_in
                        time.duration = to_hours(float(time_diff.total_seconds()))
                        time.save()
                        response_data = {
                            "message": "OK!",
                            "time_id": "",
                            "action": "time-in"
                        }
                        return render_json(response_data)
                    return HttpResponse("NO TIME RECORD FOUND")
                return HttpResponse("No Time ID")



