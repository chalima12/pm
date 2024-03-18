from django.core.management.base import BaseCommand
from pm.views import update_schedule_statuses

class Command(BaseCommand):
    help = 'Update schedule statuses at the end of each quarter'

    def handle(self, *args, **options):
        update_schedule_statuses()
        self.stdout.write(self.style.SUCCESS('Schedule statuses updated successfully'))
