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
        # Fetch existing instance if the record already exists
        if self.pk:
            existing_instance = SavingAccount.objects.get(pk=self.pk)
            
            # Handle loan operations
            loan_account = self.owner.loan_accounts.first()
            if loan_account:
                # Check if there's a loan value to add
                if self.loan > 0:
                    loan_account.loan_balance += self.loan  # Add loan to the balance
                
                # Check if there's a repayment to deduct
                if self.loan_repay > 0:
                    loan_account.loan_balance -= self.loan_repay  # Subtract loan repayment
                    loan_account.loan_balance = max(loan_account.loan_balance, 0)  # Ensure no negative balance
                
                loan_account.save()  # Save the loan account after updates

            # Handle interest operations
            interest_account = self.owner.interest_accounts.first()
            if interest_account:
                # Check if there's an interest value to add
                if self.interest > 0:
                    interest_account.interest_balance += self.interest  # Add interest to the balance

                # Check if there's an interest repayment to deduct
                if self.interest_repay > 0:
                    interest_account.interest_balance -= self.interest_repay  # Subtract interest repayment
                    interest_account.interest_balance = max(interest_account.interest_balance, 0)  # Ensure no negative balance

                interest_account.save()  # Save the interest account after updates

            # Handle commodity operations
            commodity_account = self.owner.commodity_accounts.first()
            if commodity_account:
                # Check if there's a commodity value to add
                if self.commod > 0:
                    commodity_account.commod_balance += self.commod  # Add commodity to the balance
                
                # Check if there's a commodity repayment to deduct
                if self.commod_repay > 0:
                    commodity_account.commod_balance -= self.commod_repay  # Subtract commodity repayment
                    commodity_account.commod_balance = max(commodity_account.commod_balance, 0)  # Ensure no negative balance
                
                commodity_account.save()  # Save the commodity account after updates

        else:
            # If it's a new record, simply add the normal savings to balance
            self.balance += self.normal_savings

        # Call the parent class's save method to handle other fields and logic
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

