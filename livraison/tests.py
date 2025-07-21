from django.contrib.auth import get_user_model
from django.test import TestCase

from register.views import *


# Create your tests here.
class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)


class LoginTests(TestCase):

    User = get_user_model()

    def setUp(self):
        self.credentials = {
            'email': 'normal@user.com',
            'password': 'foo'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    #TODO logout test
    def test_logout(self):
        authenticate(email='normal@user.com', password='foo')
        response = self.client.post('logout/', follow=True)
        # should be unlogged in now
        self.assertEquals(response.context['user'], None)


class RegisterTests(TestCase):

    User = get_user_model()

    def setUp(self):
        self.credentials = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'normal@user.com',
            'password': 'foo',
            'adresse': 'test'
        }

    def test_register(self):
        # send register data
        response = self.client.post('', self.credentials, follow=True)
        # should exist and be logged now
        self.assertTrue(User.objects.filter(email='normal@user.com') is not None)
