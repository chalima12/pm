from django.contrib import admin
from pm.models import Bank,Schedule,Terminal,User

# admin.site.register(Bank)
# admin.site.register(User)
# admin.site.register(Terminal)
# admin.site.register(Schedule)
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display =['bank_name','bank_key']
    # list_editable =['bank_key']
    list_per_page =10

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =['first_name','last_name','gender','phone','email','address']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display =['bank_name','terminal_name','end_date','assign_to','status']

@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ['bank_name','moti_district','tid','terminal_name','serial_number','location','city']

