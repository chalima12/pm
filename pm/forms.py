from django import forms
from pm.models import Terminal, Bank, User, Schedule


class TerminalForm(forms.ModelForm):
    class Meta:
        model = Terminal
        fields = ['bank_name', 'bank_district', 'bank_branch', 'moti_district', 'tid',
                  'terminal_name', 'serial_number', 'model', 'disspenser_type', 'city', 'location']
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
        fields = ['first_name', 'last_name', 'gender',
                  'username', 'email', 'phone', 'address']
        MALE = 'M'
        FEMALE = 'F'
        gender_choices = [
            (MALE, 'Male'),
            (FEMALE, 'Female'),
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'})
        }


class ScheduleForm(forms.ModelForm):

    # terminal_name = forms.ModelMultipleChoiceField(queryset=Terminal.objects.all(
    # ),  widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=True, help_text ="Select ATMS")

    class Meta:
        model = Schedule
        fields = ['terminals', 'start_date', 'end_date', 'description']
        widgets = {
            'terminals': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Type your description here'}),
        }


class AssignEngineerForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['priority', 'assign_to', 'material_required']
        widgets = {
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assign_to': forms.Select(attrs={'class': 'form-control'}),
            'material_required': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter Materials Used here...'}),

        }


class EndScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['comment', 'checklist_photo', 'closed_date']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter Comment here...'}),
            'checklist_photo': forms.FileInput(attrs={'class': 'form-control', }),
            'closed_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
