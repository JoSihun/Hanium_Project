from django.urls import path, re_path
from . import views

urlpatterns =[
    path('developer/', views.developer, name='developer'),
    path('', views.index, name='index'),
############################################################################
    path('freeboard/', views.freeboard_list, name='freeboard'),
    path('freeboard/detail/<int:pk>/', views.post_detail, name='boarddetail'),
    path('freeboard/edit/<int:pk>/', views.post_edit, name='boardedit'),
    path('freeboard/delete/<int:pk>/', views.post_delete, name='boarddelete'),
    path('freeboard/writing/', views.writing, name='writing'),
############################################################################
    path('function/', views.function, name='function'),
    path('grammar/', views.grammar, name='grammar'),
    path('plagiarism/', views.plagiarism, name='plagiarism'),
    path('pass/', views.pass_or_fail, name='pass'),
    path('grammar/detail/<int:pk>/', views.grammar_detail, name='grammar_result'),
    path('plagiarism/detail/<int:pk>/', views.plagiarism_detail, name='plagiarism_result'),
    path('pass/detail/<int:pk>/', views.pass_or_fail_detail, name='pass_result'),
    path('recommend/', views.recommend, name='recommend'),
############################################################################
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password/', views.password, name='password'),
    path('register/', views.register, name='register'),
############################################################################
    path('myinfo/', views.myinfo, name='myinfo'),
    path('myinfo/modify',views.pass_modify, name='modify'),
############################################################################
    path('myintro/',views.myintro_list,name='myintro'),
    path('myintro/detail/<int:pk>/', views.myintro_detail, name='introdetail'),
    path('myintro/edit/<int:pk>/', views.myintro_edit, name='introedit'),
    path('myintro/delete/<int:pk>/', views.myintro_delete, name='introdelete'),
############################################################################
]