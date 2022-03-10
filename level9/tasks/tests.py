import email
from django.test import TestCase, RequestFactory
from rest_framework import status
from django.contrib.auth.models import User

class ViewTestCases(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',email="test@gmail.com")
        self.user.set_password('test')
        self.user.save()
        
    def test_view_user_login(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_user_signup(self):
        response = self.client.get("/user/signup/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)