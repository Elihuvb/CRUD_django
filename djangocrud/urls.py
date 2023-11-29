"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name="home"),
    path('task/', views.task, name="task"),
    path('task/complete_list/', views.task_complete_list, name="task_complete_list"),
    path('task/create/', views.new_task, name="new_task"),
    path('task/<int:task_id>/', views.task_detail, name="task_detail"),
    path('task/<int:task_id>/complete-', views.task_delete, name="task_delete"),
    path('task/<int:task_id>/delete-', views.task_complete, name="task_complete"),
    path('logout/', views.signout, name="logout"),
    path('signup/', views.singup, name="signup"),
    path('signin/', views.signin, name="signin"),
]
