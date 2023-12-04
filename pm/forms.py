from django import forms
from pm.models import Terminal, Bank, User, AllSchedule,ScheduleList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
# from .managers import CustomUserManager
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['gender'].required = True
        self.fields['phone'].required = True
        self.fields['address'].required = True
    first_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: First Name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: Last Name', widget=(
        forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.', widget=(
        forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_('Just Enter the same password, for confirmation'))
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender','username', 'email','phone', 'address','password1', 'password2']
        
        widgets = {    
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TerminalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_name'].required = True
        self.fields['moti_district'].required = True
        self.fields['terminal_name'].required = True
        self.fields['city'].required = True
        self.fields['location'].required = True

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_name'].required = True
        self.fields['bank_key'].required = True

    class Meta:
        model = Bank
        fields = ['bank_name', 'bank_key']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_key': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AllScheduleForm():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].required = True
    # terminals = forms.ModelMultipleChoiceField(queryset=Terminal.objects.all(
    # ), widget=forms.SelectMultiple(attrs={'class': 'form-control select2 select2bs4'}))
    class Meta:
        model = AllSchedule
        fields = ['schedule_name', 'created_by', 'start_date', 'description']
        widgets = {
            'schedule_name':forms.TextInput(attrs={'class': 'form-control'}),
            'created_by': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Type your description here'}),
        }


class ScheduleListForm(forms.ModelForm):
    terminals = forms.ModelMultipleChoiceField(queryset=Terminal.objects.all(
    ), widget=forms.SelectMultiple(attrs={'class': 'form-control select2 select2bs4'}))
    class Meta:
        model = ScheduleList
        fields = ['terminals']
# class AssignEngineerForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['priority'].required = True
#         self.fields['assign_to'].required = True

#     class Meta:
#         model = Schedule
#         fields = ['priority', 'assign_to', 'material_required']
#         widgets = {
#             'priority': forms.Select(attrs={'class': 'form-control'}),
#             'assign_to': forms.Select(attrs={'class': 'form-control'}),
#             'material_required': forms.Textarea(
#                 attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter Materials Used here...'}),

#         }


# class EndScheduleForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['comment'].required = True

#     class Meta:
#         model = Schedule
#         fields = ['comment', 'checklist_photo', 'closed_date']
#         widgets = {
#             'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter Comment here...'}),
#             'checklist_photo': forms.FileInput(attrs={'class': 'form-control'}),
#             'closed_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
#         }
