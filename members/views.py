from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .forms import MemberCreateForm
from savings.models import (SavingDeposit,
        SavingWithdrawal)

from savings.models import SavingAccount, LoanAccount, InterestAccount, CommodityAccount

from loans.models import (LoanIssue,
        LoanPayment,)
from shares.models import (ShareAccount,ShareSell,
        ShareBuy,)
from django.contrib.auth.decorators import user_passes_test
from .forms import MembershipAccountForm, StaffAccountEditForm, MembershipAccountEditForm
from django.contrib import messages
from .models import Member, Message, Notification
from .forms import LoginForm, MessageForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate against Member model
            try:
                member = Member.objects.get(username=username)
                if check_password(password, member.password):  # Use check_password for manual password verification
                    member.last_login = timezone.now()  # Update last_login manually
                    member.save(update_fields=['last_login'])  # Save only the last_login field
                    
                    # Log the user in
                    login(request, member, backend='django.contrib.auth.backends.ModelBackend')
                    
                    # Redirect based on user role
                    if member.is_superuser:
                        return redirect('members:admin_dashboard')  # Redirect to admin dashboard
                    elif member.is_staff:
                        return redirect('staff_dashboard')  # Redirect to staff dashboard
                    else:
                        return redirect('members:dashboard')  # Redirect to member dashboard
            except Member.DoesNotExist:
                messages.error(request, 'Invalid login credentials')
    else:
        form = LoginForm()
    
    return render(request, 'members/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('members:login')  # Redirect to the login page or any page after logout


def MemberAccountRegister(request):
    members = Member.objects.all()
    if request.method == 'POST':
        form = MembershipAccountForm(request.POST, request.FILES)
        username = request.POST.get('username')

        # Check if the username already exists
        if Member.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
        else:
            if form.is_valid():
                member = form.save(commit=False)
                member.save()
                messages.success(request, 'You successfully registered')
                return redirect('members:login')
            else:
                print("DEBUG: Form is invalid")
                print(form.errors)
                messages.error(request, 'There was an error with your submission. Please try again.')

    else:
        form = MembershipAccountForm()

    context = {'form': form, 'members': members}
    return render(request, 'members/membershipaccount.html', context)


def member_create(request):
    template = 'members/form.html'

    form = MemberCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('members:member')

    context = {
            'form': form,
            'title': "Create",
            }

    return render(request, template, context)



def member(request):
    # Exclude members who are staff or superusers
    members_list = Member.objects.filter(is_staff=False, is_superuser=False).order_by("mem_number")
    
    # Get the number of members per page from the request, default is 10
    per_page = request.GET.get('per_page', 10)
    
    # Paginate the members list, showing 'per_page' members per page
    paginator = Paginator(members_list, per_page)
    page_number = request.GET.get('page')

    try:
        members = paginator.page(page_number)
    except PageNotAnInteger:
        members = paginator.page(1)  # If page is not an integer, deliver first page
    except EmptyPage:
        members = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page

    context = {
        'members': members,
    }

    # Render the full template with the table inside it
    return render(request, 'members/members.html', context)





def member_detail(request, mem_number):
    template = 'members/member_details.html'

    member = get_object_or_404(Member, mem_number=mem_number)
    saving_ac = get_object_or_404(SavingAccount, owner=member)
    deposit_transactions = SavingDeposit.objects.filter(account=saving_ac, delete_status = False)
    withdrawal_transactions = SavingWithdrawal.objects.filter(account=saving_ac, delete_status = False)
    loan_ac = get_object_or_404(LoanAccount, owner=member)
    pending_loan = LoanIssue.objects.filter(account=loan_ac, status="Pending", delete_status = False)
    approved_loan = LoanIssue.objects.filter(account=loan_ac, status="Approved", delete_status = False)
    issue_transactions = LoanIssue.objects.filter(account=loan_ac, delete_status = False)
    payment_transactions = LoanPayment.objects.filter(loan_num__account=loan_ac, delete_status = False)
    share_ac = get_object_or_404(ShareAccount, owner=member)
    sell_transactions = ShareSell.objects.filter(account=share_ac, delete_status = False)
    buy_transactions = ShareBuy.objects.filter(account=share_ac, delete_status = False)

    context = {
            'member': member,
            'saving_ac': saving_ac,
            'loan_ac': loan_ac,
            'share_ac': share_ac,
            'pending_loan': pending_loan,
            'approved_loan': approved_loan,
            'deposit_transactions': deposit_transactions,
            'withdrawal_transactions': withdrawal_transactions,
            'issue_transactions': issue_transactions,
            'payment_transactions': payment_transactions,
            'sell_transactions': sell_transactions,
            'buy_transactions': buy_transactions,
    }

    return render(request, template, context)




@login_required
def MemberDashboardView(request):
    template = 'members/members_dashboard.html'

    # Fetch all saving accounts for the logged-in user
    savings = SavingAccount.objects.filter(owner=request.user)

    # Aggregate the total received amount for the user
    savings_sum = savings.aggregate(Sum('balance'))['balance__sum']

    # Sort transactions by date
    sorted_savings = savings.order_by('-date_created')

    # Helper function to get balance from an account model
    def get_balance(account_class, user, balance_field):
        accounts = account_class.objects.filter(owner=user)
        if accounts.exists():
            balance_sum = accounts.aggregate(Sum(balance_field))[f'{balance_field}__sum']
            return balance_sum if balance_sum is not None else 0
        return 0  # Return 0 if no account found

    # Fetch the loan, interest, and commodity balances for the logged-in user
    loan_balance = get_balance(LoanAccount, request.user, 'loan_balance')
    interest_balance = get_balance(InterestAccount, request.user, 'interest_balance')
    commod_balance = get_balance(CommodityAccount, request.user, 'commod_balance')

    # Fetch the balance fields from the SavingAccount model
    balance_sum = savings.aggregate(Sum('balance'))['balance__sum']
    divine_touch_sum = savings.aggregate(Sum('divine_touch'))['divine_touch__sum']
    sp_sav_sum = savings.aggregate(Sum('sp_sav'))['sp_sav__sum']
    rss_sum = savings.aggregate(Sum('rss'))['rss__sum']

    context = {
        'transactions': sorted_savings,
        'transactions_sum': savings_sum,
        'loan_balance': loan_balance,
        'interest_balance': interest_balance,
        'commod_balance': commod_balance,
        'balance_sum': balance_sum,
        'divine_touch_sum': divine_touch_sum,
        'sp_sav_sum': sp_sav_sum,
        'rss_sum': rss_sum,
        'member': request.user,
        'title': "My Savings & Loans",
    }

    return render(request, template, context)


    

def Dashboard(request):
    template = 'members/dashboard.html'

    return render(request, template)


def home(request):
    # Count the number of members who are not staff and not superusers
    non_staff_users_count = Member.objects.filter(is_staff=False, is_superuser=False).count()
    
    # Count the total number of saving accounts
    saving_accounts_count = SavingAccount.objects.count()
    
    context = {
        'non_staff_users_count': non_staff_users_count,
        'saving_accounts_count': saving_accounts_count,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            
            # Create notification for the recipient
            Notification.objects.create(
                user=message.recipient,  # Assuming 'recipient' is a field in your Message model
                message=f"You have a new message from {request.user.username}"
            )
            
            messages.success(request, 'Message Sent successfully')
            #return redirect('some_view_name')  # Redirect to prevent form resubmission
    else:
        form = MessageForm()

    return render(request, 'members/send_message.html', {'form': form})


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-date_sent')
    print("Messages:", messages)  # This will print messages to the console
    print(request.user)
    return render(request, 'members/inbox.html', {'messages': messages})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = message.sender  # Reply to the original sender
            reply.is_reply = True
            reply.save()
            messages.success(request, 'Reply Sent successfully')
    else:
        form = ReplyForm()

    return render(request, 'members/view_message.html', {'message': message, 'form': form})


@login_required
def member_inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-date_sent')
    sent_messages = Message.objects.filter(sender=request.user, is_reply=False).order_by('-date_sent')
    replies = Message.objects.filter(recipient=request.user, is_reply=True).order_by('-date_sent')  # Replies from admins

    # Count unread replies from the admin
    unread_replies_count = Message.objects.filter(recipient=request.user, is_reply=True, is_read=False).count()

    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'replies': replies,
        'unread_replies_count': unread_replies_count,  # Pass count to template
    }
    return render(request, 'members/member_inbox.html', context)


@login_required
def MemberAccountEditView(request):
    member = request.user

    if member.is_staff or member.is_superuser:
        return redirect('members:staff_edit_account')

    if request.method == 'POST':
        form = MembershipAccountEditForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            # Check if the password has changed
            if 'password' in form.cleaned_data:
                password = form.cleaned_data['password']
                # Hash the new password
                if not password.startswith('pbkdf2_sha256$'):
                    member.password = make_password(password)
                else:
                    member.password = password
            form.save()
            messages.success(request, 'Your account has been updated successfully.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MembershipAccountEditForm(instance=member)

    context = {'form': form}
    return render(request, 'members/edit_account.html', context)



@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def StaffAccountEditView(request):
    staff_member = request.user

    if request.method == 'POST':
        form = StaffAccountEditForm(request.POST, request.FILES, instance=staff_member)
        if form.is_valid():
            # Check if the password has changed
            if 'password' in form.cleaned_data:
                password = form.cleaned_data['password']
                # Hash the new password if it's not already hashed
                if not password.startswith('pbkdf2_sha256$'):
                    staff_member.password = make_password(password)
                else:
                    staff_member.password = password
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = StaffAccountEditForm(instance=staff_member)

    context = {'form': form}
    return render(request, 'members/staff_edit_account.html', context)


@user_passes_test(lambda u: u.is_superuser)
def AddStaffMemberView(request):
    if request.method == 'POST':
        form = StaffAccountEditForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.is_staff = True
            if form.cleaned_data.get('is_superuser'):
                member.is_superuser = True
            member.save()
            messages.success(request, 'New staff/superuser member has been added successfully.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = StaffAccountEditForm()

    context = {'form': form}
    return render(request, 'members/add_staff_member.html', context)


def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})

def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})  # Respond with success