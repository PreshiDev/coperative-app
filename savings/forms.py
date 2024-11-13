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
    # Fields to add/subtract values
    add_savings = forms.FloatField(required=False, initial=0)
    subtract_savings = forms.FloatField(required=False, initial=0)
    add_divine_touch = forms.FloatField(required=False, initial=0)
    subtract_divine_touch = forms.FloatField(required=False, initial=0)
    add_rss = forms.FloatField(required=False, initial=0)
    subtract_rss = forms.FloatField(required=False, initial=0)
    add_share = forms.FloatField(required=False, initial=0)
    subtract_share = forms.FloatField(required=False, initial=0)

    class Meta:
        model = SavingAccount
        fields = [
            'owner', 'received', 'loan_repay', 'interest_repay', 'commod_repay',
            'loan', 'interest', 'commod', 'month', 'year'
        ]
        widgets = {
            'owner': Select2Widget(),
            'received': forms.NumberInput(attrs={'class': 'form-control'}),
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
        # Exclude admin and staff users, then order alphabetically by last name, then by first name
        self.fields['owner'].queryset = (
            Member.objects.exclude(is_staff=True, is_superuser=True)
            .order_by('last_name', 'first_name')
        )
        self.fields['owner'].label_from_instance = self.get_display_name

    def get_display_name(self, obj):
        # Format as "Last Name, First Name"
        return f"{obj.last_name} {obj.first_name}"
    
    def clean(self):
        cleaned_data = super().clean()

        # Update balance fields by adding the values from add/subtract inputs to the current instance balance
        cleaned_data['savings_balance'] = (
            self.instance.savings_balance + cleaned_data.get('add_savings', 0) - cleaned_data.get('subtract_savings', 0)
        )
        cleaned_data['divine_touch_balance'] = (
            self.instance.divine_touch_balance + cleaned_data.get('add_divine_touch', 0) - cleaned_data.get('subtract_divine_touch', 0)
        )
        cleaned_data['rss_balance'] = (
            self.instance.rss_balance + cleaned_data.get('add_rss', 0) - cleaned_data.get('subtract_rss', 0)
        )
        cleaned_data['share_balance'] = (
            self.instance.share_balance + cleaned_data.get('add_share', 0) - cleaned_data.get('subtract_share', 0)
        )

        # Ensure no negative values in balance fields
        for field in ['savings_balance', 'divine_touch_balance', 'rss_balance', 'share_balance',
                    'loan_balance', 'interest_balance', 'commodity_balance']:
            if cleaned_data.get(field, 0) < 0:
                self.add_error(field, f"{field.replace('_', ' ').capitalize()} cannot be negative.")

        return cleaned_data



class SavingAccountEditForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = [
            'owner', 'month', 'year', 'received', 'savings', 
            'divine_touch', 'rss', 'loan', 'interest', 'commod', 
            'loan_repay', 'share', 'commod_repay', 'interest_repay' # Adjust fields as requested
        ]
        widgets = {
            'owner': Select2Widget(),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'received': forms.NumberInput(attrs={'class': 'form-control'}),
            'savings': forms.NumberInput(attrs={'class': 'form-control'}),
            'divine_touch': forms.NumberInput(attrs={'class': 'form-control'}),
            'rss': forms.NumberInput(attrs={'class': 'form-control'}),
            'share': forms.NumberInput(attrs={'class': 'form-control'}),
            'loan': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest': forms.NumberInput(attrs={'class': 'form-control'}),
            'commod': forms.NumberInput(attrs={'class': 'form-control'}),
            'loan_repay': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_repay': forms.NumberInput(attrs={'class': 'form-control'}),
            'commod_repay': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SavingAccountEditForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Member.objects.exclude(is_staff=True, is_superuser=True)

        # Format number fields with commas for display
        for field_name in ['received', 'savings', 'divine_touch', 'rss', 'loan', 'interest', 'commod', 'loan_repay', 'interest_repay', 'commod_repay']:
            if self.instance and getattr(self.instance, field_name, None) is not None:
                self.fields[field_name].initial = "{:,}".format(getattr(self.instance, field_name))

    def clean(self):
        cleaned_data = super().clean()
        # Remove commas before saving the data
        for field_name in ['received', 'savings', 'divine_touch', 'rss', 'loan', 'interest', 'commod', 'loan_repay', 'interest_repay', 'commod_repay']:
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

