from django import forms
from pm.models import Terminal, Bank, User, BankBranch, Schedule


class TerminalForm(forms.ModelForm):
    class Meta:
        model = Terminal
        fields = ['bank_name', 'bank_district', 'bank_branch', 'moti_district', 'tid',
                  'terminal_name', 'serial_number', 'model', 'disspenser_type', 'city', 'location']
        labels: {
            'bank_name': 'Bank Name',
            'bank_district': 'Bank District',
            'bank_branch': 'Bank Branch',
            'moti_district': 'Moti District',
            'tid': 'Terminal ID',
            'terminal_name': 'Termianl Name',
            'serial_number': 'Serial Number',
            'model': 'Termianl Model',
            'disspenser_type': 'Dispenser Type',
            'city': 'City',
            'location': 'Location'
        }
        widgets = {
            'bank_name': forms.Select(attrs={'class': 'form-control'}),
            'bank_district': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'moti_district': forms.Select(attrs={'class': 'form-control'}),
            'tid': forms.TextInput(attrs={'class': 'form-control'}),
            'terminal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'disspenser_type': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'})


        }


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'bank_key']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_key': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','gender','username','email','phone','address']
        MALE = 'M'
        FEMALE = 'F'
        gender_choices = [
            (MALE, 'Male'),
            (FEMALE, 'Female'),
        ]
        widgets ={
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'username':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'})
        }


class BankBranchForm(forms.ModelForm):
    class Meta:
        model = BankBranch
        fields = "__all__"


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['bank_name', 'terminal_name', 'start_date',
                  'end_date', 'assign_to', 'status', 'description']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['bank_name', 'terminal_name', 'start_date','end_date', 'description']
        widgets = {
            'bank_name': forms.Select(attrs={'class': 'form-control'}),
            'terminal_name': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter description here...'}),
        }

        
