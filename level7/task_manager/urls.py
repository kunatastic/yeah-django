"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from tasks.apiview import TaskViewSet, HistoryViewSet
from tasks.views import *

from rest_framework_nested import routers
router = SimpleRouter()

router.register("api/task", TaskViewSet)
# router.register("api/history", HistoryViewSet)

task_router = routers.NestedSimpleRouter(router, "api/task", lookup="task")
task_router.register("history", HistoryViewSet)

urlpatterns = [

    # ADMIN
    path("admin/", admin.site.urls),
    # path("historyapi/", HistoryListApi.as_view()),
    # path("taskapi/", TaskListApi.as_view()),

    # AUTH
    path("user/signup/", UserCreateView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/logout/", LogoutView.as_view()),

    # TASKS
    path("tasks/", PendingTaskView.as_view()),
    path("add-task/", AddTaskView.as_view()),
    path("update-task/<pk>/", UpdateTaskView.as_view()),
    path("delete-task/<pk>/", DeleteTaskView.as_view()),
    path("completed-tasks/", CompletedTaskView.as_view()),
    path("all-tasks/", AllTaskView.as_view()),

    path("", PendingTaskView.as_view()),

] + router.urls + task_router.urls
