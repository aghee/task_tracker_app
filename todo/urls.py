from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,logoutUser,Registration
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LogoutView


urlpatterns=[
    path("",TaskList.as_view(),name="all_tasks"),
    path("login/",CustomLoginView.as_view(),name="login"),
    path("register/",Registration.as_view(),name="register"),
    path("logout/",logoutUser,name="logout"),
    # path("logout/",LogoutView.as_view(next_page="login"),name="logout"),

    path("reset_password/",auth_views.PasswordResetView.as_view(template_name="todo/password_reset.html"),name="password_reset"),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name="todo/password_reset_sent.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="todo/password_reset_form.html"),name="password_reset_confirm"),
    path("reset_password_complete",auth_views.PasswordResetCompleteView.as_view(template_name="todo/password_reset_complete.html"),name="password_reset_complete"),

    path("task/<int:pk>/",TaskDetail.as_view(),name="detailtask"),
    path("task-create/",TaskCreate.as_view(),name="createtask"),
    path("task-update/<int:pk>",TaskUpdate.as_view(),name="updatetask"),
    path("task-delete/<int:pk>",TaskDelete.as_view(),name="deletetask"),
]