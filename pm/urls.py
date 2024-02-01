from . import views
# from django.contrib.auth.decorators import permission_required
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),
    path('banks/', views.banks, name='banks-page'),
    path('banks/addBank/', views.addBank, name='add-bank'),
    path('banks/update_bank/<int:bank_id>', views.updateBank, name="update-bank"),
    path('banks/inactive_bank/<int:bank_id>',views.deactivate_bank, name='inactive_bank'),
    path('banks/active_bank/<int:bank_id>', views.activate_bank, name='active-bank'),
    
    path('terminals/', views.terminals, name="all-terminals"),
    path('view_terminal/<int:id>', views.view_terminal, name='view_terminal'),
    path('add-terminal/', views.addTerminal, name='add-terminal'),
    path('update_terminal/<int:terminal_id>',
         views.updateTerminal, name='update-terminal'),
    # path('schedules/', views.schedule, name='schedules'),
    path('all-schedules', views.all_schedule, name='schedules'),
    path('all-schedules/', views.all_schedule, name='schedules'),
    path('detail_schedule/<int:pk>',views.detail_schedules_list, name='detail_schedules_list'),

    path('assign_engineer/<int:id>', views.assign_engineer, name='assign-engineer'),
    path("start_task/<int:scheule_id>", views.start_task, name="start-task"),
    path('end_scheduled_task/<int:id>',
         views.end_scheduled_task, name='end-task'),
    path('approve_task/<int:id>', views.approve_task, name='task_approval'),
    path('reject_task/<int:id>', views.reject_task, name='reject_task'),
    path('users/', views.user, name='all-engineers'),
    path('users_list', views.user_card_display, name ="users-card"),
    path('create_user/', views.add_user, name = "create_user"),
    path('your_tasks/', views.user_specific_tasks, name='your-task' ),
    path('profile/', views.userProfile, name="profile"),
    path('edit_user/<int:user_id>', views.edit_user, name='edit-user'),
    path('view-user/<int:id>', views.view_user, name='view-user'),
    path('change_password/', views.change_password, name="change-password"),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path("add_moti_district/",views.add_moti_district, name="add-moti-district"),
    path("moti_districts/", views.moti_districts, name="districts-list"),
    path('update_district/<int:district_id>', views.update_moti_district, name="update-moti-district"),

    # Reports URL
    path("report/users", views.engineers_list, name="engineers-list"),
    path("report/banks", views.banks_list, name="bank-list"),
    path("report/terminals", views.terminals_list, name="terminals-list"),
    path("banks/<int:bank_id>", views.schedules_detail_report, name="schedules-report"),
    path('assign_permissions/<int:user_id>',views.assign_permissions, name="assign-permisions"),
    path("reports/districts",views.districts_list,name="districts-report"),
    path("districts/<int:district_id>",views.schedule_report_by_district, name="schedule-by-district"),
]

# from . import views
# # from django.contrib.auth.decorators import permission_required
# from django.urls import path
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('banks/', views.banks, name='banks-page'),
#     path('banks/addBank/', views.addBank, name='add-bank'),
#     path('banks/update_bank/<int:bank_id>', views.updateBank, name="update-bank"),
#     path('banks/inactive_bank/<int:bank_id>',
#          views.deactivate_bank, name='inactive_bank'),
#     path('banks/active_bank/<int:bank_id>', views.activate_bank, name='active-bank'),

#     path('terminals/', views.terminals, name="all-terminals"),
#     path('terminals/view_terminal/<int:id>', views.view_terminal, name='view_terminal'),
#     path('terminals/add-terminal/', views.addTerminal, name='add-terminal'),
#     path('terminals/update_terminal/<int:terminal_id>',
#          views.updateTerminal, name='update-terminal'),
#     # path('schedules/', views.schedule, name='schedules'),
# #     path('all-schedules', views.all_schedule, name='schedules'),
#     path('schedules/', views.all_schedule, name='schedules'),
#     path('schedules/detail_schedule/<int:pk>',views.detail_schedules_list, name='detail_schedules_list'),

#     path('schedules/assign_engineer/<int:id>', views.assign_engineer, name='assign-engineer'),
#     path("schedules/start_task/<int:scheule_id>", views.start_task, name="start-task"),
#     path('schedules/end_scheduled_task/<int:id>',
#          views.end_scheduled_task, name='end-task'),
#     path('schedules/approve_task/<int:id>', views.approve_task, name='task_approval'),
#     path('schedules/reject_task/<int:id>', views.reject_task, name='reject_task'),

#     path('users/', views.user, name='all-engineers'),
#     path('users/users_list/', views.user_card_display, name ="users-card"),
#     path('users/create_user/', views.add_user, name = "create_user"),
#     path('your_tasks/', views.user_specific_tasks, name='your-task' ),
#     path('profile/', views.userProfile, name="profile"),
#     path('users/edit_user/<int:user_id>', views.edit_user, name='edit-user'),
#     path('users/view-user/<int:id>', views.view_user, name='view-user'),
#     path('change_password/', views.change_password, name="change-password"),
#     path('schedules/create_schedule/', views.create_schedule, name='create_schedule'),

#     # Reports URL

#     path("report/users", views.engineers_list, name="engineers-list"),
#     path("report/banks", views.banks_list, name="bank-list"),
#     path("report/terminals", views.terminals_list, name="terminals-list"),
#     path("banks/<int:bank_id>", views.schedules_detail_report, name="schedules-report"),
#     path('assign_permissions/<int:user_id>',
#          views.assign_permissions, name="assign-permisions")
# ]