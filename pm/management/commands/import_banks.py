import os
import pandas as pd
from django.core.management.base import BaseCommand
from pm.models import Bank  # Adjust the import based on your app name
from django.db import connection
from datetime import datetime

class Command(BaseCommand):
    help = 'Import bank data from an Excel file, clearing existing data and resetting IDs'

    def handle(self, *args, **kwargs):
        # Path to the uploaded file relative to the manage.py file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../Bank-2024-07-09.xlsx')

        # Clear all existing data from the Bank model
        Bank.objects.all().delete()

        # Reset the ID sequence for different databases
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute("ALTER SEQUENCE pm_bank_id_seq RESTART WITH 1;")
            elif connection.vendor == 'sqlite':
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='pm_bank';")
            elif connection.vendor == 'mysql':
                cursor.execute("ALTER TABLE pm_bank AUTO_INCREMENT = 1;")
            else:
                self.stdout.write(self.style.ERROR('Unsupported database vendor'))
                return

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Iterate over the rows of the DataFrame and create Bank objects
        for index, row in df.iterrows():
            bank = Bank(
                bank_name=row['name'],
                bank_key=row['key'],
                is_active=True,
                created_date=datetime.now().date()
            )
            bank.save()
            self.stdout.write(self.style.SUCCESS(f'Created bank: {bank.bank_name}'))

        self.stdout.write(self.style.SUCCESS('Bank data import complete.'))
