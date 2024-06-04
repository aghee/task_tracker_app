# from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
# from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# from django.contrib.auth import get_user_model

# Create your views here.
class CustomLoginView(LoginView):
    template_name="todo/login.html"
    fields="__all__"
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy("all_tasks")
    
# class CustomLogoutView(LogoutView):
#     def get_success_url(self):
#         return reverse_lazy("login")

# def loginUser(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password,backend="django.contrib.auth.backends.ModelBackend")
#     if user is not None:
#         login(request, user)
#         return redirect("all_tasks")
#     else:
#         print("Incorrect credentials!Try again.")

def logoutUser(request):
    logout(request)
    return redirect("login")


class Registration(FormView):
    template_name="todo/register.html"
    form_class=UserCreationForm
    # redirect_authenticated_user=True
    success_url=reverse_lazy("all_tasks")
    
    #ensure user is loggedin once the form is submitted
    #user is created,logged in and redirected
    #use same concept for Google SignIn
    def form_valid(self,form):
        user=form.save()
        # User=get_user_model()
        # user=User.objects.create_user(
        #     username=form.cleaned_data["username"],
        #     password=form.cleaned_data["password"],
        #     backend="django.contrib.auth.backends.ModelBackend",
        # )
        if user is not None:
            login(self.request,user)
        return super(Registration,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("all_tasks")
        return super(Registration,self).get(*args,**kwargs)

#default template:_list.html, context=object_list-can be overriden
class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name="tasks"
    
    #ensure user gets their data only
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tracker']='TASK TRACKER'
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(status="Completed").count()
        context['count_one']=context['tasks'].filter(status="In-progress").count()
        context['count_two']=context['tasks'].filter(status="Discontinued").count()

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
            # context['tasks']=context['tasks'].filter(title__startswith=search_input)
        
        context['search_input']=search_input
        return context


#default template:_detail.html, context=object-can be overriden
class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name="task"
    template_name="todo/task.html"

#default template:_form.html, context=object-can be overriden
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    # fields='__all__'
    # exclude='user'
    fields=['title','description','status']
    success_url=reverse_lazy('all_tasks')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

#default template:_form.html context=object -can be overriden
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','status']
    success_url=reverse_lazy('all_tasks')

#default template:_confirm_delete.html context=object -can be overriden
class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    # fields='__all__'
    success_url=reverse_lazy('all_tasks')
    template_name="todo/task_confirmation_delete.html"

    