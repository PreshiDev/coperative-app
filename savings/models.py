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
    received = models.PositiveIntegerField(default=0)
    
    # Existing fields
    savings = models.PositiveIntegerField(default=0)
    divine_touch = models.PositiveIntegerField(default=0)
    rss = models.PositiveIntegerField(default=0)
    loan_repay = models.PositiveIntegerField(default=0)
    interest_repay = models.PositiveIntegerField(default=0)
    commod_repay = models.PositiveIntegerField(default=0)
    loan = models.PositiveIntegerField(default=0)
    interest = models.PositiveIntegerField(default=0)
    commod = models.PositiveIntegerField(default=0)
    share = models.PositiveIntegerField(default=0)
    
    # New balance fields
    savings_balance = models.PositiveIntegerField(default=0)
    interest_balance = models.PositiveIntegerField(default=0)
    loan_balance = models.PositiveIntegerField(default=0)
    commodity_balance = models.PositiveIntegerField(default=0)
    rss_balance = models.PositiveIntegerField(default=0)
    divine_touch_balance = models.PositiveIntegerField(default=0)
    share_balance = models.PositiveIntegerField(default=0)
    
    month = models.IntegerField(choices=MONTH_CHOICES, default=datetime.date.today().month)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.date.today().year)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



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

