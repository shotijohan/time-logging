from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from timelogger.models import TimeInTimeOut
from django.views.generic import View

from timelogger.views import to_hours


class TimeInTimeOutTestCase(TestCase, View):
    def setUp(self):
        user = User.objects.create_user(
            username='juandelacruz',
            email='juandelacruz@gmail.com',
            first_name='Juan',
            last_name='Dela Cruz',
            password='juantamad'
        )
        time = TimeInTimeOut()
        time.user = user
        time.time_in = timezone.now()
        time.save()

    def test_time_in(self):
        user = User.objects.all()[0]
        time = TimeInTimeOut()
        time.user = user
        time.time_in = timezone.now()
        time.save()

        self.assertTrue(time, isinstance(time, TimeInTimeOut))

        self.assertEqual(time.duration, 0.0)

    def test_time_out(self):
        time = TimeInTimeOut.objects.all()[0]
        if time.duration == 0.0:
            time.time_out = timezone.now()
            time_diff = time.time_out - time.time_in
            time.duration = to_hours(float(time_diff.total_seconds()))
            time.save()

        self.assertNotEqual(time.duration, 0)
