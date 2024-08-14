import os
import pandas as pd
from django.core.management.base import BaseCommand
from pm.models import Bank, Terminal, Moti_district # Adjust the import based on your app name
from datetime import datetime

class Command(BaseCommand):
    help = 'Import terminal data from an Excel file, clearing existing data and resetting IDs'

    def handle(self, *args, **kwargs):
        # Path to the uploaded file relative to the manage.py file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../Terminal-2024-07-09.xlsx')

        # Clear all existing data from the Terminal model
        Terminal.objects.all().delete()
        
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Iterate over the rows of the DataFrame and create Terminal objects
        for index, row in df.iterrows():
            # Try to get the Bank instance using the primary key or ID
            try:
                bank = Bank.objects.get(id=row['bank'])
            except Bank.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Bank with ID '{row['bank']}' does not exist. Skipping row {index}."))
                continue

            # Try to get the Moti_district instance using the primary key or ID
            try:
                moti_district = Moti_district.objects.get(id=row['moti_district'])
            except Moti_district.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Moti district with ID '{row['moti_district']}' does not exist. Skipping row {index}."))
                continue

            # Create the Terminal instance
            terminal = Terminal(
                bank_name=bank,
                district=moti_district,
                tid=row['terminal_Number'],
                terminal_name=row['name'],
                serial_number=row['serial_Number'],
                disspenser_type=row['Dispenser_type'],
                city=row['city'],
                created_date=datetime.now().date()
            )
            terminal.save()
            self.stdout.write(self.style.SUCCESS(f'Created terminal: {terminal.terminal_name}'))

        self.stdout.write(self.style.SUCCESS('Terminal data import complete.'))
