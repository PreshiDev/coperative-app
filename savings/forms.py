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


from django.forms.utils import pretty_name
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma

class SavingDepositForm(forms.ModelForm):
    # Fields to add/subtract values
    add_savings = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtract_savings = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    add_divine_touch = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtract_divine_touch = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    add_rss = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtract_rss = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    add_share = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtract_share = forms.CharField(required=False, initial='0', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SavingAccount
        fields = [
            'owner', 'received', 'loan_repay', 'interest_repay', 'commod_repay',
            'loan', 'interest', 'commod', 'month', 'year'
        ]
        widgets = {
            'owner': Select2Widget(),
            'received': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
            'loan': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
            'interest': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
            'commod': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
            'loan_repay': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
            'interest_repay': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
            'commod_repay': forms.TextInput(attrs={'class': 'form-control'}),  # Change to TextInput
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

        # Preformat initial values with intcomma
        for field_name, field in self.fields.items():
            if field_name in ['received', 'loan', 'interest', 'commod', 'loan_repay', 'interest_repay', 'commod_repay']:
                if self.initial.get(field_name) is not None:
                    self.initial[field_name] = intcomma(self.initial[field_name])

    def get_display_name(self, obj):
        # Format as "Last Name, First Name"
        return f"{obj.last_name} {obj.first_name}"

    def clean(self):
        cleaned_data = super().clean()

        # Fields to clean (those that could contain commas)
        fields_to_clean = [
            'received', 'loan', 'interest', 'commod',
            'loan_repay', 'interest_repay', 'commod_repay',
            'add_savings', 'subtract_savings',
            'add_divine_touch', 'subtract_divine_touch',
            'add_rss', 'subtract_rss',
            'add_share', 'subtract_share'
        ]

        for field in fields_to_clean:
            value = cleaned_data.get(field)
            if value is not None and isinstance(value, str):
                try:
                    # Remove commas and convert to float
                    cleaned_data[field] = float(value.replace(',', ''))
                except ValueError:
                    self.add_error(field, f"Invalid format for {field}. Please enter a numeric value.")

        # Compute balances and validate them
        balance_fields = [
            ('savings_balance', 'add_savings', 'subtract_savings'),
            ('divine_touch_balance', 'add_divine_touch', 'subtract_divine_touch'),
            ('rss_balance', 'add_rss', 'subtract_rss'),
            ('share_balance', 'add_share', 'subtract_share')
        ]

        for balance_field, add_field, subtract_field in balance_fields:
            balance = (
                self.instance.__dict__.get(balance_field, 0) +
                cleaned_data.get(add_field, 0) -
                cleaned_data.get(subtract_field, 0)
            )
            cleaned_data[balance_field] = balance

            # Validate that balances are not negative
            if balance < 0:
                self.add_error(balance_field, f"{balance_field.replace('_', ' ').capitalize()} cannot be negative.")

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

