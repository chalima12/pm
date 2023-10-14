from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
urlpatterns = [
    path('', views.home, name='home'),
    path('banks/', views.banks, name='banks-page'),
    path('banks/<int:id>/', views.view_bank, name='view-bank'),
    path('addBank/', views.addBank, name='add-bank'),
    path('update_bank/<int:bank_id>', views.updateBank, name="update-bank"),
    path('bank_detail/<int:bank_id>', views.bank_detail, name='bank-detail'),
    path('terminals/', views.terminals, name="all-terminals"),
    path('add-terminal/', views.addTerminal, name='add-terminal'),
    path('update_terminal/<int:terminal_id>',
         views.updateTerminal, name='update-terminal'),
    path('schedules/', views.schedule, name='schedules'),
    path('make-schedule/', views.makeSchedule, name='make-schedule'),
    path('reports/', views.reports, name='reports'),
    path('engineers/', views.user, name='all-engineers'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),


]
