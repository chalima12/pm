from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
urlpatterns = [
    path('', views.home, name='home'),
    path('banks/', views.banks, name='banks-page'),
    path('terminals/', views.terminals, name="all-terminals"),
    path('schedule/', views.schedule, name='creat-schedule'),
    path('reports/', views.reports, name='reports'),
    path('engineers/', views.engineers, name='all-engineers'),
    path('add-terminal/', views.addTerminal, name= 'add-terminal')
]
