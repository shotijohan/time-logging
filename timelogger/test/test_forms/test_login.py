from django.contrib.auth import authenticate
from django.test import TestCase
from timelogger.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='juandelacruz',
            email='juandelacruz@gmail.com',
            first_name='Juan',
            last_name='Dela Cruz',
            password='juantamad'
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

        user2 = authenticate(
            username="juandelacruz",
            password="juantamad"
        )

        self.assertEquals(user, None)
        self.assertEquals(user2.is_authenticated(), True)