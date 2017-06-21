from pprint import pprint

import logging
from django.contrib.auth import authenticate
from django.test import TestCase
from timelogger.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test",
            email="test",
            first_name="test",
            last_name="test",
            password="test"
        )

    def test_authenticate(self):
        """
        User can be authenticated
        :return: boolean
        """
        user = authenticate(
            username="test",
            password="test"
        )

        self.assertEquals(user.is_authenticated(), True)