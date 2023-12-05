from . import views
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),
    path('banks/', views.banks, name='banks-page'),
    path('addBank/', views.addBank, name='add-bank'),
    path('update_bank/<int:bank_id>', views.updateBank, name="update-bank"),
    path('inactive_bank/<int:bank_id>', views.deactivate_bank, name='inactive_bank'),
    path('active_bank/<int:bank_id>', views.activate_bank, name='active-bank'),
    path('terminals/', views.terminals, name="all-terminals"),
    path('view_terminal/<int:id>', views.view_terminal, name='view_terminal'),
    path('add-terminal/', views.addTerminal, name='add-terminal'),
    path('update_terminal/<int:terminal_id>',views.updateTerminal, name='update-terminal'),
    # path('schedules/', views.schedule, name='schedules'),
    path('all-schedules', views.all_schedule, name='schedules'),
    path('detail_schedule/<int:scheule_id>',views.detail_schedules_list, name='detail_schedules_list'),
    path('assign_engineer/<int:id>', views.assign_engineer, name='assign-engineer'),
    path("start_task/<int:scheule_id>", views.start_task, name="start-task"),
    path('end_scheduled_task/<int:id>',views.end_scheduled_task, name='end-task'),
    path('show-checklist/<int:id>', views.task_appoval,name='task_approval'),
    path('users/', views.user, name='all-engineers'),
    path('add-user/', views.create_user, name="add-user"),
    path('edit_user/<int:user_id>', views.edit_user,name='edit-user'),
    path('view-user/<int:id>', views.view_user, name='view-user'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('reports/', views.reports, name='reports'),

    # Reports URL

    path("report/users", views.engineers_list, name="engineers-list" ),
    path("report/banks", views.banks_list, name="bank-list"),
    path("report/terminals", views.terminals_list, name="terminals-list"),
    path("report/schedules", views.schedule_list, name="schedules-list"),
    

]
