"""DeepSquare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

import deepsquareapp.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', deepsquareapp.views.index, name='index'),
    path('login/', deepsquareapp.views.login, name='login'),
    path('logout/', deepsquareapp.views.logout, name='logout'),
    path('password/', deepsquareapp.views.password, name='password'),
    path('repassword/', deepsquareapp.views.repassword, name='repassword'),
    path('resetpassword/', deepsquareapp.views.resetpassword, name='resetpassword'),
    path('signup/', deepsquareapp.views.signup, name='signup'),
    path('insert/', deepsquareapp.views.initial_data_insert, name='InitialData'),

    path('myinfo/', deepsquareapp.views.myinfo, name='myinfo'),
    path('myinfo_edit/', deepsquareapp.views.myinfo_edit, name='myinfo_edit'),

    path('selfintroboard/', deepsquareapp.views.selfintroboard, name='selfintroboard'),
    path('selfintroboard_writing/', deepsquareapp.views.selfintroboard_writing, name='selfintroboard_writing'),
    path('selfintroboard_save/<int:pk>', deepsquareapp.views.selfintroboard_save, name='selfintroboard_save'),
    path('selfintroboard_post/<int:pk>', deepsquareapp.views.selfintroboard_post, name='selfintroboard_post'),
    path('selfintroboard_edit/<int:pk>', deepsquareapp.views.selfintroboard_edit, name='selfintroboard_edit'),
    path('selfintroboard_delete/<int:pk>', deepsquareapp.views.selfintroboard_delete, name='selfintroboard_delete'),
    path('selfintroboard_result/<int:pk>', deepsquareapp.views.selfintroboard_result, name='selfintroboard_result'),

    path('freeboard/', deepsquareapp.views.freeboard, name='freeboard'),
    path('freeboard_writing/', deepsquareapp.views.freeboard_writing, name='freeboard_writing'),
    path('freeboard_post/<int:pk>', deepsquareapp.views.freeboard_post, name='freeboard_post'),
    path('freeboard_edit/<int:pk>', deepsquareapp.views.freeboard_edit, name='freeboard_edit'),
    path('freeboard_delete/<int:pk>', deepsquareapp.views.freeboard_delete, name='freeboard_delete'),

    path('questionboard/', deepsquareapp.views.questionboard, name='questionboard'),
    path('questionboard_writing/', deepsquareapp.views.questionboard_writing, name='questionboard_writing'),
    path('questionboard_post/<int:pk>', deepsquareapp.views.questionboard_post, name='questionboard_post'),
    path('questionboard_edit/<int:pk>', deepsquareapp.views.questionboard_edit, name='questionboard_edit'),
    path('questionboard_delete/<int:pk>', deepsquareapp.views.questionboard_delete, name='questionboard_delete'),
]