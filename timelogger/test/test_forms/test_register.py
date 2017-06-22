from django.test import TestCase
from timelogger.models import User


class TestRegistration(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='juandelacruz',
            email='juandelacruz@gmail.com',
            first_name='Juan',
            last_name='Dela Cruz',
            password='juantamad'
        )

    def test_registration(self):
        """
        Test Registration for User's Model
        :return:
        """

        self.assertEqual(len(User.objects.all()), 1)


