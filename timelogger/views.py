# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import View
from .constants import *


# Create your views here.
class Login(View):
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'timelogger/home.html')
        return render(request, 'timelogger/login.html')

    def post(self, request):
        post_data = request.POST
        if post_data:
            pprint(post_data)
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
            user = User.objects.create_user(
                username=post_data.get('username'),
                email=post_data.get('email'),
                first_name=post_data.get('first_name'),
                last_name=post_data.get('last_name'),
                password=post_data.get('password'),
            )
            if user:
                return HttpResponse("SUCCESS")
            else:
                return HttpResponse(user)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect("/")
