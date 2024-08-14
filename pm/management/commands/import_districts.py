import os
import pandas as pd
from django.core.management.base import BaseCommand
from pm.models import Bank ,Terminal,Moti_district # Adjust the import based on your app name
from django.db import connection
from datetime import datetime


class Command(BaseCommand):
    help = 'Import districts from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            
            # Delete existing data (optional)
            Moti_district.objects.all().delete()
            
            # Reset primary key sequence to 1
            Moti_district.objects.raw('ALTER TABLE moti_district AUTO_INCREMENT = 1;')
            
            # Iterate over each row and create District objects
            for index, row in df.iterrows():
    # Map 'name' column from Excel to 'district_name' field in the model
                district_name = row['name']
                region = row['region']
    # Create District object with the correct field
                district = Moti_district.objects.create(district_name=district_name, region=region)
                self.stdout.write(self.style.SUCCESS(f'District created: {district}'))
                
                self.stdout.write(self.style.SUCCESS('Districts imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
