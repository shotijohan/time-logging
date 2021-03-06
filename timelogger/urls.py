from django.conf.urls import url

from .views import Login, TimeInTimeOutHandler
from .views import Register
from .views import Logout
from .views import API

urlpatterns = [
    url(r'^$', Login.as_view(), name='index'),
    url(r'^register', Register.as_view(), name='register'),
    url(r'^register-member', Register.as_view(), name='register-member'),
    url(r'^login', Login.as_view(), name='login'),
    url(r'^logout', Logout.as_view(), name='login'),
    url(r'^timer-start-end', TimeInTimeOutHandler.as_view(), name="timer-start-end"),
    url(r'^api/v1/timeintimeout', API.as_view(), name="API")
    # url(r'^$',
    #     ListView.as_view(queryset=User_accounts.objects.all().order_by("-created_date")[:25],
    #                      template_name="timelogger/home.html"
    #                      )),
]
