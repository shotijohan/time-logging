from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from timelogger.models import TimeInTimeOut
from django.views.generic import View


class TestUpdateDescription(TestCase, View):
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

    def test_update_description(self):
        user = User.objects.all()[0]
        time = TimeInTimeOut.objects.all()[0]
        time.user = user
        time.time_out = timezone.now()
        time.description = "Test Description"
        time.save()

        self.assertTrue(time, isinstance(time, TimeInTimeOut))

        self.assertEqual(time.description, "Test Description")