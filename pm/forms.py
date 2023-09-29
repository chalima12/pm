from django import forms
from pm.models import Terminal,Bank,Engineer,BankBranch

class TerminalForm(forms.ModelForm):
    class Meta:
        model =Terminal
        fields ="__all__"
class BankForm(forms.ModelForm):
    class Meta:
        modele = Bank
        fields = ['bank_name','bank_key']
        labels ={
            'bank_name':"Bank Name",
            'bank_key':"Bank Key"
        }
        widgets ={
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_key': forms.TextInput(attrs={'class': 'form-control'}),
        }
class EngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields ="__all__"
class BankBranchForm(forms.ModelForm):
    class Meta:
        model =BankBranch
        fields = "__all__"