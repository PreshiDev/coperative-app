from django.shortcuts import render
from django.db.models import Sum, F, Q
from members.models import Member
from savings.models import SavingAccount, LoanAccount, InterestAccount, CommodityAccount  # Update the import based on your app structure

# Create your views here.


def home(request):
    # Count the number of members who are not staff and not superusers
    non_staff_users_count = Member.objects.filter(is_staff=False, is_superuser=False).count()

    # Count the total number of saving accounts where the owner is not staff and not a superuser
    saving_accounts_count = SavingAccount.objects.filter(
        owner__is_staff=False, owner__is_superuser=False
    ).count()

    # Count the number of unique users with a loan balance greater than zero
    pending_loans_count = LoanAccount.objects.filter(
        loan_balance__gt=0
    ).values('owner').distinct().count()

    # Count the number of unique users with an interest balance greater than zero
    pending_interests_count = InterestAccount.objects.filter(
        interest_balance__gt=0
    ).values('owner').distinct().count()

    # Count the number of unique users with a commodity balance greater than zero
    pending_commodities_count = CommodityAccount.objects.filter(
        commod_balance__gt=0
    ).values('owner').distinct().count()

    context = {
        'non_staff_users_count': non_staff_users_count,
        'saving_accounts_count': saving_accounts_count,
        'pending_loans_count': pending_loans_count,  # Add this to the context
        'pending_interests_count': pending_interests_count,  # Add this to the context
        'pending_commodities_count': pending_commodities_count,  # Add this to the context
    }

    return render(request, 'static_pages/home.html', context)


def about(request):
    template = 'static_pages/about.html'

    return render(request, template)

def contact(request):
    template = 'static_pages/contact.html'

    return render(request, template)

