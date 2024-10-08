from django.contrib import admin
from pm.models import Bank, Schedule, Terminal, User, AllSchedule, Moti_district


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'bank_key']
    # list_editable =['bank_key']
    list_per_page = 10
@admin.register(AllSchedule)
class AllScheduleAdmin(admin.ModelAdmin):
    list_display = ['schedul_name', 'scheduled_by']
    # list_editable =['bank_key']
    list_per_page = 10


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'gender', 'phone', 'email', 'address']



@admin.register(Schedule)
class ScheduleListAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'status', 'closed_date',]


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'district', 'tid',
                    'terminal_name', 'serial_number', 'location', 'city']

@admin.register(Moti_district)
class Moti_districtAdmin(admin.ModelAdmin):
    list_display=["district_name","location","region"]