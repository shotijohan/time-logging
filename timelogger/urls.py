from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from timelogger.models import User_accounts
from . import views

urlpatterns = [
    # url(r'^', views.index, name='index'),
    url(r'^$',
        ListView.as_view(queryset=User_accounts.objects.all().order_by("-created_date")[:25],
                         template_name="timelogger/home.html"
                         )),
]
