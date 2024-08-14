@echo off
REM Change directory to your project folder
cd C:\Users\Administrator\Documents\pm_project

REM Activate virtual environment
call C:\Users\Administrator\Documents\pm_project\.venv\Scripts\activate.bat

REM Start the Django development server
python manage.py runserver 0.0.0.0:80


pause


