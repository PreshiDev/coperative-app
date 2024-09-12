from django.db import models
from members.models import Member
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime


# Create your models here.

ACCOUNT_STATUS_CHOICE = (
        ('Deactivated', 'Deactivated'),
        ('Activated', 'Activated'),
        )

DELETE_STATUS_CHOICE = (
        ('False', 'False'),
        ('True', 'True'),
        )


SAVING_TYPE_CHOICES = [
    ('Oracle', 'Oracle'),
    ('Teller', 'Teller'),
]

MONTH_CHOICES = [
    (1, "January"), (2, "February"), (3, "March"), (4, "April"),
    (5, "May"), (6, "June"), (7, "July"), (8, "August"),
    (9, "September"), (10, "October"), (11, "November"), (12, "December")
]

YEAR_CHOICES = [(r, r) for r in range(2000, datetime.date.today().year+1)]



class SavingAccount(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='saving_accounts')
    payment_type = models.CharField(choices=SAVING_TYPE_CHOICES, max_length=6, default='Oracle')
    received = models.PositiveIntegerField(default=0)
    normal_savings = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
    divine_touch = models.PositiveIntegerField(default=0)
    sp_sav = models.PositiveIntegerField(default=0)
    rss = models.PositiveIntegerField(default=0)
    loan_repay = models.PositiveIntegerField(default=0)
    interest_repay = models.PositiveIntegerField(default=0)
    commod_repay = models.PositiveIntegerField(default=0)
    loan = models.PositiveIntegerField(default=0)  # New field for loan addition
    interest = models.PositiveIntegerField(default=0)  # New field for interest addition
    commod = models.PositiveIntegerField(default=0)  # New field for commodity addition
    month = models.IntegerField(choices=MONTH_CHOICES, default=datetime.date.today().month)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.date.today().year)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Only adjust balance if it's a new record or normal_savings has changed
        if self.pk:
            # Fetch the existing instance to get the current normal_savings
            existing_instance = SavingAccount.objects.get(pk=self.pk)
            if self.normal_savings != existing_instance.normal_savings:
                self.balance += self.normal_savings - existing_instance.normal_savings
        else:
            self.balance += self.normal_savings
        
        # Deduct loan repayment from the LoanAccount
        loan_account = self.owner.loan_accounts.first()
        if loan_account and self.loan_repay > 0:
            loan_account.loan_balance -= self.loan_repay
            loan_account.loan_balance = max(loan_account.loan_balance, 0)  # Ensure no negative balance
            loan_account.loan += self.loan
            loan_account.save()

        # Deduct interest repayment from the InterestAccount
        interest_account = self.owner.interest_accounts.first()
        if interest_account and self.interest_repay > 0:
            interest_account.interest_balance -= self.interest_repay
            interest_account.interest_balance = max(interest_account.interest_balance, 0)  # Ensure no negative balance
            interest_account.interest += self.interest
            interest_account.save()

        # Deduct commodity repayment from the CommodityAccount
        commodity_account = self.owner.commodity_accounts.first()
        if commodity_account and self.commod_repay > 0:
            commodity_account.commod_balance -= self.commod_repay
            commodity_account.commod_balance = max(commodity_account.commod_balance, 0)  # Ensure no negative balance
            commodity_account.commod += self.commod
            commodity_account.save()

        super(SavingAccount, self).save(*args, **kwargs)



class LoanAccount(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loan_accounts')
    loan = models.PositiveIntegerField(default=0)  # You can replace this with your choices
    loan_balance = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} - Loan Account"


class InterestAccount(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='interest_accounts')
    interest = models.PositiveIntegerField(default=0)
    interest_balance = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} - Interest Account"


class CommodityAccount(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='commodity_accounts')
    commod = models.PositiveIntegerField(default=0)
    commod_balance = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} - Commodity Account"


class SavingDeposit(models.Model):
    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.owner.first_name

class SavingWithdrawal(models.Model):
    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.owner.first_name

@receiver(post_save, sender=Member)
def create_account(sender, **kwargs):
    if kwargs['created']:
        # Remove the current_balance argument
        SavingAccount.objects.create(owner=kwargs['instance'])

