
from datetime import datetime
from pytz import timezone
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from tasks.views import EmailReminderView, STATUS_CHOICES,  AddTaskView, PendingTaskView, UpdateTaskView, CompletedTaskView, AllTaskView, DeleteTaskView
from tasks.models import Task, Report, History
from rest_framework import status
from tasks.tasks import send_email_reminder, reset_recurring_reports


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="Kunal", email="kunal@task-manager.org")
        self.user.set_password("SafePasword123")
        self.user.save()

    def test_user_create_view(self):
        response = self.client.get("/user/signup/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_view(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_pending_tasks_no_access(self):
        request = self.factory.get("/tasks/")
        request.user = AnonymousUser()
        response = PendingTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/user/login?next=/tasks/")
    
    def test_view_pending_tasks_with_access(self):
        request = self.factory.get("/tasks/")
        request.user = self.user
        response = PendingTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_view_completed_tasks_with_access(self):
        request = self.factory.get("/completed-tasks/")
        request.user = self.user
        response = CompletedTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_view_all_tasks_with_access(self):
        request = self.factory.get("/all-tasks/")
        request.user = self.user
        response = AllTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_add_task_no_access(self):
        request = self.factory.get("/add-task/")
        request.user = AnonymousUser()
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/user/login?next=/add-task/")

    def test_view_add_task_with_access(self):
        request = self.factory.get("/add-task/")
        request.user = self.user
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_view_add_task(self):
        request = self.factory.post("/add-task/",
            {
                "title": "Homework",
                "description": "Maths and English",
                "priority": 1,
                "completed": False,
                "status": STATUS_CHOICES[0][0],
            })
        request.user = self.user
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/tasks/")
        self.assertEqual(Task.objects.get(priority=1).title, "Homework")


    def test_view_add_task_with_invalid_data(self):
        request = self.factory.post("/add-task/",
            {
                "title": "",
                "description": "",
                "priority": 1,
                "completed": False,
                "status": STATUS_CHOICES[0][0],
            })
        request.user = self.user
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_add_task_with_negative_prioirty(self):
        request = self.factory.post("/add-task/",
            {
                "title": "Homework",
                "description": "Maths and English",
                "priority": -1,
                "completed": False,
                "status": STATUS_CHOICES[0][0],
            })
        request.user = self.user
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_add_task_with_cascade_logic(self):
        request = self.factory.post("/add-task/",
            {
                "title": "Shopping",
                "description": "Tomato and Orange",
                "priority": 1,
                "completed": False,
                "status": STATUS_CHOICES[2][0],
            })
        request.user = self.user
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/tasks/")
        self.assertEqual(Task.objects.get(priority=1).title, "Shopping")

        request = self.factory.post("/add-task/",
            {
                "title": "Sleep",
                "description": "Minimum 8 hours",
                "priority": 1,
                "completed": False,
                "status": STATUS_CHOICES[2][0],
            })
        request.user = self.user
        response = AddTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/tasks/")
        self.assertEqual(Task.objects.get(priority=1).title, "Sleep")
    

    def test_view_update_task(self):
        Task(
            title="Go for a walk",
            description="Walk to the park",
            priority=2,
            completed=False,
            status=STATUS_CHOICES[0][0],
            user=self.user
        ).save()
        task = Task.objects.get(priority=2)
        request = self.factory.get(f"/update-task/{task.pk}/")
        request.user = self.user
        response = UpdateTaskView.as_view()(request, pk=task.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_view_update_task_update_priority(self):
        Task(
            title="Go for a walk",
            description="Walk to the park",
            priority=2,
            completed=False,
            status=STATUS_CHOICES[0][0],
            user=self.user
        ).save()
        task = Task.objects.get(priority=2)
        request = self.factory.post(f"/update-task/{task.pk}/",
            {
                "title": "Go for a walk",
                "description": "Walk to the park",
                "priority": 1,
                "completed": False,
                "status": STATUS_CHOICES[0][0],
            })
        request.user = self.user
        response = UpdateTaskView.as_view()(request, pk=task.pk)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/tasks/")
        self.assertEqual(Task.objects.get(priority=1).title, "Go for a walk")



    def test_view_delete_task(self):
        Task(
            title="Go for a walk",
            description="Walk to the park",
            priority=2,
            completed=False,
            status=STATUS_CHOICES[0][0],
            user=self.user
        ).save()
        task = Task.objects.get(priority=2)
        request = self.factory.post(f"/delete-task/{task.pk}/")
        request.user = self.user
        response = DeleteTaskView.as_view()(request, pk=task.pk)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/tasks/")



    
    def test_email_reminder_view(self):
        report = Report.objects.filter(user=self.user).first()
        request = self.factory.get(f"/reminder/{report.pk}/")
        request.user = self.user
        response = EmailReminderView.as_view()(request, pk=report.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_reminder_view_with_invalid_user(self):
        try:
            request = self.factory.get(f"/reminder/45848543805/")
            request.user = self.user
            response = EmailReminderView.as_view()(request, pk=45848543805)
            self.assertTrue(False)
        except:
            self.assertFalse(False)


class ModelsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="Kunal", email="kunal@task-manager.org")
        self.user.set_password("SafePasword123")
        self.user.save()
    
    def test_models_tasks(self):
        Task(
            title="Car wash",
            description="Wash the car",
            priority=56,
            completed=False,
            status=STATUS_CHOICES[0][0],
        ).save()
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(str(Task.objects.get(priority=56)),"Car wash 56 False")

    def test_models_history(self):
        Task(
            title="Car wash",
            description="Wash the car",
            priority=56,
            completed=False,
            status=STATUS_CHOICES[0][0],
        ).save()

        History(
            task=Task.objects.get(priority=56),
            status_previous = STATUS_CHOICES[0][0],
            status_current = STATUS_CHOICES[1][0],
        ).save()

        self.assertEqual(History.objects.count(), 1)
        self.assertEqual(str(History.objects.get(task=Task.objects.get(priority=56))), "Car wash PENDING IN_PROGRESS")

    def test_models_report(self):
        now_time = datetime.now()
        report = Report(
            notify_at=now_time,
            user = self.user,
            recurring = True,
        )
        report.save()
        print(Report.objects.get(pk=report.pk))
        self.assertEqual(Report.objects.count(), 2)


class CeleryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="Kunal", email="kunal@task-manager.org")
        self.user.set_password("SafePasword123")
        self.user.save()
    
    def test_celery_task(self):
        try:
            send_email_reminder()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_celery_task_with_email_report_recurring(self):
        report = Report.objects.filter(user=self.user).first()
        report.notify_at = datetime.now(timezone("Asia/Kolkata"))
        report.recurring = True
        report.enabled = True
        report.save()
        try:
            send_email_reminder()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
    
    def test_celery_task_with_email_report_not_recurring(self):
        report = Report.objects.filter(user=self.user).first()
        report.notify_at = datetime.now(timezone("Asia/Kolkata"))
        report.recurring = False
        report.enabled = True
        report.save()
        try:
            send_email_reminder()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    
    def test_reset_recurring_reports(self):
        try:
            reset_recurring_reports()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
