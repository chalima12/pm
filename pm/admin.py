from django.contrib import admin
from pm.models import Bank,Schedule,Terminal,User

# admin.site.register(Bank)
# admin.site.register(User)
# admin.site.register(Terminal)
# admin.site.register(Schedule)
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    pass

