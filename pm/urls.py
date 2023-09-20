from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
urlpatterns = [
    path('', views.home),
    path('Banks', views.allBanks),
    path('Atms', views.atms),
    path('Schedule', views.makeSchedule),
    path('index',views.index),
    path('chart', views.chart, name = 'chart')

   
]
