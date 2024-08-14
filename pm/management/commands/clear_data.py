from django.core.management.base import BaseCommand
from django.db import connection
from pm.models import Moti_district,Terminal,Bank

class Command(BaseCommand):
    help = 'Clear all data from the table and reset the primary key sequence'

    def handle(self, *args, **kwargs):
        # Delete all data from the table
        Terminal.objects.all().delete()

        # Reset the primary key sequence to start from 1
        sequence_name =  Terminal._meta.db_table + '_id_seq'
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
            cursor.execute(f"SELECT setval('{sequence_name}', 1, false)")

        self.stdout.write(self.style.SUCCESS('Data cleared and primary key sequence reset'))