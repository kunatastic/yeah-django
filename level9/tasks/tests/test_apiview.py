from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from tasks.models import Task, STATUS_CHOICES
from rest_framework import status

class ApiViewTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="Kunal", email="kunal@task-manager.org")
        self.user.set_password("SafePasword123")
        self.user.save()

    def test_task_view_set(self):
        self.client.login(username="Kunal", password="SafePasword123")
        task = Task(
            title="Test Task",
            description="Test Description",
            completed=False,
            user = self.user,
            priority = 1,
            status = STATUS_CHOICES[0][0]
        )
        task.save()
        response = self.client.get('/api/task/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'/api/task/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_history_view_set(self):
        self.client.login(username="Kunal", password="SafePasword123")
        task = Task(
            title="Test Task",
            description="Test Description",
            completed=False,
            user = self.user,
            priority = 1,
            status = STATUS_CHOICES[0][0]
        )
        task.save()
        task.status = STATUS_CHOICES[1][0]
        task.save()
        response = self.client.get(f'/api/task/{task.id}/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    