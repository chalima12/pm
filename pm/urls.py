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
    path('schedules/', views.schedule, name='schedules'),
    path('assign_engineer/<int:id>', views.assign_engineer, name='assign-engineer'),
    path('end_scheduled_task/<int:id>',views.end_scheduled_task, name='end-task'),
    path('engineers/', views.user, name='all-engineers'),
    path('add-user/', views.add_user, name="add-user"),
    path('edit_user/<int:user_id>', views.edit_user,name='edit-user'),
    path('view-user/<int:id>', views.view_user, name='view-user'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('reports/', views.reports, name='reports'),

    # Reports URL

    path("report/users_list", views.engineers_list, name="engineers-list" ),
    path("report/banks_list", views.banks_list, name="bank-list"),
]
