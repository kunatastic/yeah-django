


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import (BooleanField, CharField, CheckboxInput, IntegerField,
                          ModelForm, NumberInput, Textarea, TextInput,
                          ValidationError)
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from tasks.models import Task
from tasks.cascade import cascade_logic

# Create your views here.

# CUSTOM AUTH FORM 
class GenericSignupFormView(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(GenericSignupFormView, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "rounded-md relative block w-full px-3 py-2 my-2 bg-gray-100"

class GenericLoginFormView(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(GenericLoginFormView, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "rounded-md relative block w-full px-3 py-2 my-2 bg-gray-100"

# SIGNIN USER
'''
    @url: /user/login/
    public: True
'''
class UserCreateView(CreateView):
    form_class = GenericSignupFormView
    success_url = "/user/login/"
    template_name = 'registration/signup.html'

# LOGIN USER
'''
    @url: /user/login/
    public: True
'''
class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = GenericLoginFormView
    success_url = "/tasks/"


# VIEW ADD A NEW TASK PAGE
'''
    @url: /add-tasks/
    public: False
'''

# Task create form
class TaskCreationForm(ModelForm):

    common_style = 'bg-slate-100 my-2 w-full px-4 py-2 rounded-lg text-gray-900'

    # https://stackoverflow.com/questions/20986798/django-modelform-label-customization
    title = CharField(widget=TextInput(attrs={'class': common_style, 'placeholder': 'Title'}))
    description = CharField(widget=Textarea(attrs={'class': common_style, 'placeholder': 'Description'}))
    priority = IntegerField(widget=NumberInput(attrs={'class': common_style, 'placeholder': 'Priority'}))
    completed = BooleanField(widget=CheckboxInput(attrs={'class': common_style + 'form-checkbox h-4 w-4'}), required=False)
    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if priority < 0:
            raise ValidationError("Priority must be greater than 0")
        return priority
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'completed')


# View task create form
class AddTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskCreationForm
    template_name = 'tasks/add_task.html'
    success_url = '/tasks/'
    def form_valid(self, form):
        cascade_logic(self.request.user, form.cleaned_data['priority'])
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# VIEW UPDATE A TASK PAGE
''' 
    @url: /update-task/<pk>/
    public: False
'''
class UpdateTaskView(LoginRequiredMixin ,UpdateView):
    model = Task
    form_class = TaskCreationForm
    template_name = 'tasks/update_task.html'
    success_url = '/tasks/'
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted = False)
    def form_valid(self, form):
        if (self.object.priority != form.cleaned_data['priority']):
            cascade_logic(self.object.user, form.cleaned_data['priority'])
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# DELETE A TASK
'''
    @url: /delete-task/<pk>/
    public: False
'''
class DeleteTaskView(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = '/tasks/'
    def form_valid(self, form):
        self.object.update(deleted=True)
        return HttpResponseRedirect(self.get_success_url())
    def get_queryset(self) :
        return Task.objects.filter(user=self.request.user, deleted=False)


# LIST THE COMPLETED TASK
'''
    @url: /completed-tasks/
    public: False
'''
class CompletedTaskView(LoginRequiredMixin,ListView):
    template_name = 'completed_tasks.html'
    context_object_name = 'completed'
    def get_queryset(self):
        return Task.objects.filter(deleted = False, completed = True).order_by("priority")


# LIST ALL TASKS
'''
    @url: /all-tasks/
    public: False
'''
class AllTaskView(LoginRequiredMixin,ListView):
    template_name = 'home/all_tasks.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(deleted = False, user = self.request.user).order_by("priority")

# LIST COMPLETED TASKS
'''
    @url: /completed-tasks/
    public: False
'''
class CompletedTaskView(LoginRequiredMixin,ListView):
    template_name = 'home/completed_tasks.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(deleted = False, user = self.request.user, completed = True).order_by("priority")

# LIST THE PENDING TASK
'''
    @url: /tasks/
    public: False
'''
class PendingTaskView(LoginRequiredMixin,ListView):
    template_name = 'home/pending_tasks.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(deleted = False, user = self.request.user, completed = False).order_by("priority")  