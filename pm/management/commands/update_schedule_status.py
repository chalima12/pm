from django.core.management.base import BaseCommand
from django.utils import timezone
from pm.models import Schedule

class Command(BaseCommand):
    help = 'Update remaining days of schedules'

    def handle(self, *args, **kwargs):
        schedules = Schedule.objects.all()
        today = timezone.now().date()
        for schedule in schedules:
            remaining_days = (schedule.end_date - today).days
            if remaining_days >= 0:
                if remaining_days < 5:
                    if remaining_days == 1:
                        remaining_days_str = '1 day left'
                    else:
                        remaining_days_str = f'{remaining_days} days left'
                else:
                    remaining_days_str = f'{remaining_days} days'

                schedule.remaining_days = remaining_days
                schedule.save()
                self.stdout.write(self.style.SUCCESS(f'{remaining_days_str} remaining for schedule {schedule.id}'))
            else:
                delay_days = abs(remaining_days)
                if delay_days == 1:
                    delay_str = '1 day delayed'
                else:
                    delay_str = f'{delay_days} days delayed'

                schedule.remaining_days = 0
                schedule.save()
                self.stdout.write(self.style.ERROR(f'{delay_str} for schedule {schedule.id}'))

