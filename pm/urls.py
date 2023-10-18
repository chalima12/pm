from . import views
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),
    path('banks/', views.banks, name='banks-page'),
    path('addBank/', views.addBank, name='add-bank'),
    path('update_bank/<int:bank_id>', views.updateBank, name="update-bank"),
    path('terminals/', views.terminals, name="all-terminals"),
    path('view_terminal/<int:id>', views.view_terminal, name='view_terminal'),
    path('add-terminal/', views.addTerminal, name='add-terminal'),
    path('update_terminal/<int:terminal_id>',
         views.updateTerminal, name='update-terminal'),
    path('schedules/', views.schedule, name='schedules'),
    # path('make-schedule/', views.makeSchedule, name='make-schedule'),
    path('assign_engineer/<int:id>', views.assign_engineer, name='assign-engineer'),
    path('end_scheduled_task/<int:id>',
         views.end_scheduled_task, name='end-task'),
    path('reports/', views.reports, name='reports'),
    path('engineers/', views.user, name='all-engineers'),
    path('add-user/', views.add_user, name="add-user"),
    path('view-user/<int:id>', views.view_user, name='view-user'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),


]
