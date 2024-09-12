from django import forms
from members.models import Member
from .models import (LoanIssue,LoanPayment,LoanAccount)

class LoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanAccount
        fields = ('owner', 'loan_type', 'loan', 'debit', 'credit')
    
    def clean(self):
        cleaned_data = super().clean()
        # No need to check for existing SavingAccount here
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        super(LoanAccountForm, self).__init__(*args, **kwargs)
        # Filter the owner field to exclude members who are staff or superusers
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)

class LoanIssueForm(forms.ModelForm):
    class Meta:
        model = LoanIssue
        fields = ('__all__')

class LoanPaymentForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = ('__all__')

class GetLoanNumForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = ('loan_num',)

class GetLoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanIssue
        fields = ('account',)
