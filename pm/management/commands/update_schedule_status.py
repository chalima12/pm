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
                schedule.remaining_days = remaining_days
            else:
                schedule.remaining_days = 0
            schedule.save()
        self.stdout.write(self.style.SUCCESS('Remaining days updated successfully'))
