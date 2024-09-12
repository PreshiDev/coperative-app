from django.contrib import admin
from .models import (SavingAccount,SavingDeposit,
                    SavingWithdrawal, LoanAccount, InterestAccount, CommodityAccount)

# Register your models here.
admin.site.register(SavingAccount)
admin.site.register(SavingDeposit)
admin.site.register(SavingWithdrawal)
admin.site.register(LoanAccount)
admin.site.register(InterestAccount)
admin.site.register(CommodityAccount)