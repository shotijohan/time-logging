# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from pprint import pprint

import json

from django.contrib.auth.decorators import login_required
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


def render_json(response_data, code=None):
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=(code if code else 200))


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
                return render(request, 'timelogger/login.html', {"message": INVALID_CREDENTIALS})


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


class API(View):
    def get(self, request):

        """
            Handles the /api/v1/timeintimeout end point.
            Returns list of datasets.
        """

        bottom = 5
        top = 0
        limit = 5

        response_data = {
            "code": 200,
            "type": "List of Time in and time outs",
            "method": "GET",
            "response": "OK",
            "data": [],
            "error_message": None,
            "has_more": True,
            "top": top,
            "bottom": bottom
        }
        if request.user.is_authenticated():

            if request.GET.get("bottom"):
                bottom = request.GET.get("bottom")
                if bottom:
                    bottom = int(bottom)
                response_data["bottom"] = bottom + limit

            if request.GET.get("top"):
                top = request.GET.get("top")
                if top:
                    top = int(top)
                response_data["top"] = top + limit

            query = TimeInTimeOut.objects.order_by("id").all()

            if request.GET.get("user_id") and request.GET.get("user_id") != "null":
                user_id = request.GET.get("user_id")
                query = query.filter(user_id=user_id)

            if request.GET.get("time_in"):
                try:
                    time_in = datetime.strptime(request.GET.get("time_in"), "%m/%d/%Y %H:%M")
                    query = query.filter(time_in=time_in)
                except ValueError:
                    response_data['error_message'] = 'Invalid date format for "time in"'
                    response_data['code'] = 500
                    response_data["response"] = "ValueError"
                    return render_json(response_data, code=500)

            if request.GET.get("time_out"):
                try:
                    time_out = datetime.strptime(request.GET.get("time_out"), "%m/%d/%Y %H:%M")
                    query = query.filter(time_out=time_out)
                except ValueError:
                    response_data['error_message'] = 'Invalid date format for "time_out"'
                    response_data['code'] = 500
                    response_data["response"] = "ValueError"
                    return render_json(response_data, code=500)

            if request.GET.get("start_date") and request.GET.get("end_date"):
                # try:
                start_date = datetime.strptime(request.GET.get("start_date"), "%m/%d/%Y %H:%M")
                end_date = datetime.strptime(request.GET.get("end_date"), "%m/%d/%Y %H:%M")
                query = query.filter(created_date__gte=start_date, created_date__lte=end_date)
                # except ValueError:
                #     response_data['error_message'] = 'Invalid date format for "start_date" or "end_date"'
                #     # response_data['error_message'] = str(ValueError.message)
                #     response_data['code'] = 500
                #     response_data["response"] = "ValueError"
                #     return render_json(response_data, code=500)

            if request.GET.get("first_name"):
                user_first_name = request.GET.get("first_name")
                query = query.filter(user__first_name=user_first_name)

            if request.GET.get("last_name"):
                user_last_name = request.GET.get("last_name")
                query = query.filter(user__last_name=user_last_name)

            if request.GET.get("order"):
                order = request.GET.get("order")
                try:
                    query = query.order_by(order)
                except ValueError:
                    response_data["code"] = 500
                    response_data["error_message"] = "Invalid Input for order"
                    response_data["response"] = "ValueError"
                    return render_json(response_data)

            query = query[top:bottom]
            if len(query) > 0:
                temp = []
                for q in query:
                    temp.append(q.to_object())
                response_data['data'] = temp
                return render_json(response_data)
            else:
                response_data['has_more'] = False
                return render_json(response_data)
        else:
            response_data["code"] = 500
            response_data["has_more"] = False
            response_data["error_message"] = "Unauthorized access"
            response_data["response"] = "Error"
            return render_json(response_data)

    def post(self, request):
        if request.user.is_authenticated():
            if self.request.POST.get("id"):
                time_id = self.request.POST.get("id")
                time = TimeInTimeOut.objects.get(id=int(time_id))
                if time:
                    time.description = self.request.POST.get("description")
                    time.save()
                    return render_json({"message": "GOODS"})
