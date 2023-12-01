from django.contrib import admin
from pm.models import Bank, AllSchedule, Terminal, User,ScheduleList


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'bank_key']
    # list_editable =['bank_key']
    list_per_page = 10


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'gender', 'phone', 'email', 'address']


@admin.register(AllSchedule)
class AllScheduleAdmin(admin.ModelAdmin):
    list_display = ['terminal', 'start_date', 'end_date', 'description']
@admin.register(ScheduleList)
class ScheduleListAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'status', 'closed_date',]


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'moti_district', 'tid',
                    'terminal_name', 'serial_number', 'location', 'city']
