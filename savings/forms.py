from django import forms
from django_select2.forms import Select2Widget
from members.models import Member
from django.forms.widgets import NumberInput
from django.utils import formats
from .models import (SavingDeposit,SavingWithdrawal,
        SavingAccount, LoanAccount, InterestAccount, CommodityAccount)



class LocalizedNumberInput(NumberInput):
    def format_value(self, value):
        if value is None:
            return ''
        # Format value with commas
        return formats.number_format(value, use_l10n=True)



class SavingAccountForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = '__all__'
        widgets = {
            'owner': Select2Widget(),
        }



class SavingDepositForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = [
            'owner', 'payment_type', 'received', 'normal_savings', 
            'balance', 'divine_touch', 
            'sp_sav', 'rss', 'loan_repay', 'interest_repay', 'commod_repay',
            'loan', 'interest', 'commod',  # New fields to add to the respective models
            'month', 'year'
        ]
        widgets = {
            'owner': Select2Widget(),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'received': forms.NumberInput(attrs={'class': 'form-control'}),
            'normal_savings': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'divine_touch': forms.NumberInput(),
            'sp_sav': forms.NumberInput(),
            'rss': forms.NumberInput(),
            'loan': forms.NumberInput(),
            'interest': forms.NumberInput(),
            'commod': forms.NumberInput(),
            'loan_repay': forms.NumberInput(),
            'interest_repay': forms.NumberInput(),
            'commod_repay': forms.NumberInput(),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SavingDepositForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)

        # Format number fields with commas for display
        for field_name in ['received', 'normal_savings', 'balance', 'divine_touch', 'sp_sav', 'rss', 'loan', 'interest', 'commod', 'loan_repay', 'interest_repay', 'commod_repay']:
            if self.instance and getattr(self.instance, field_name, None) is not None:
                self.fields[field_name].initial = "{:,}".format(getattr(self.instance, field_name))

    def clean(self):
        cleaned_data = super().clean()
        # Remove commas before saving the data
        for field_name in ['received', 'normal_savings', 'balance', 'divine_touch', 'sp_sav', 'rss', 'loan', 'interest', 'commod', 'loan_repay', 'interest_repay', 'commod_repay']:
            value = cleaned_data.get(field_name)
            if value:
                cleaned_data[field_name] = str(value).replace(',', '')
        return cleaned_data



class SavingAccountEditForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = [
            'owner', 'payment_type', 'month', 'year', 
            'received', 'normal_savings', 'balance', 'divine_touch', 'sp_sav', 'rss',
            'loan', 'interest', 'commod', 'loan_repay'
        ]
        widgets = {
            'owner': Select2Widget(),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'received': forms.NumberInput(attrs={'class': 'form-control'}),
            'normal_savings': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'divine_touch': forms.NumberInput(attrs={'class': 'form-control'}),
            'sp_sav': forms.NumberInput(attrs={'class': 'form-control'}),
            'rss': forms.NumberInput(attrs={'class': 'form-control'}),
            'loan': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest': forms.NumberInput(attrs={'class': 'form-control'}),
            'commod': forms.NumberInput(attrs={'class': 'form-control'}),
            'loan_repay': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SavingAccountEditForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)

        # Format number fields with commas for display
        for field_name in ['received', 'normal_savings', 'balance', 'divine_touch', 'sp_sav', 'rss', 'loan', 'interest', 'commod', 'loan_repay']:
            if self.instance and getattr(self.instance, field_name, None) is not None:
                self.fields[field_name].initial = "{:,}".format(getattr(self.instance, field_name))

    def clean(self):
        cleaned_data = super().clean()
        # Remove commas before saving the data
        for field_name in ['received', 'normal_savings', 'balance', 'divine_touch', 'sp_sav', 'rss', 'loan', 'interest', 'commod', 'loan_repay']:
            value = cleaned_data.get(field_name)
            if value:
                cleaned_data[field_name] = str(value).replace(',', '')
        return cleaned_data



class SavingWithdrawalForm(forms.ModelForm):

    class Meta:
        model = SavingWithdrawal
        fields = ('__all__')

class GetSavingAccountForm(forms.ModelForm):

    class Meta:
        model = SavingDeposit
        fields = ('account',)


class LoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanAccount
        fields = ['owner', 'loan_balance']
        widgets = {
            'owner': Select2Widget(),
            'loan_balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(LoanAccountForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)


class InterestAccountForm(forms.ModelForm):
    class Meta:
        model = InterestAccount
        fields = ['owner', 'interest_balance']
        widgets = {
            'owner': Select2Widget(),
            'interest_balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(InterestAccountForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)


class CommodityAccountForm(forms.ModelForm):
    class Meta:
        model = CommodityAccount
        fields = ['owner', 'commod_balance']
        widgets = {
            'owner': Select2Widget(),
            'commod_balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommodityAccountForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)

