from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django import forms
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .forms import (SavingDepositForm,SavingWithdrawalForm,
        GetSavingAccountForm,SavingAccountForm, SavingAccountEditForm, LoanAccountForm,
        InterestAccountForm, CommodityAccountForm)
                    
from .models import (SavingDeposit,SavingWithdrawal,
                    SavingAccount,)
import openpyxl
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.contrib.auth.decorators import login_required

# Create your views here.

def saving_account(request):
    template = 'savings/savings_form.html'

    pk = request.session['ordered_savings_pk']

    ordered_saving_ac = get_object_or_404(SavingAccount, pk=pk)

    if request.method == 'POST':
        form = SavingAccountForm(request.POST, instance=ordered_saving_ac)
    else:
        form = SavingAccountForm(instance=ordered_saving_ac)

    if form.is_valid():
        form.save()
        return redirect("savings:saving")

    context = {
            'form':form,
            'title': "de|activate",
            }

    return render(request, template, context)


# def saving_deposit(request):
#     if request.method == 'POST':
#         owner_id = request.POST.get('owner')
#         payment_type = request.POST.get('payment_type')

#         try:
#             saving_account = SavingAccount.objects.get(owner_id=owner_id, payment_type=payment_type)
#         except SavingAccount.DoesNotExist:
#             saving_account = SavingAccount(owner_id=owner_id, payment_type=payment_type)

#         # Fetch values from the form, default to 0 if none provided
#         received = float(request.POST.get('received', 0))
#         normal_savings = float(request.POST.get('normal_savings', 0))
#         divine_touch = float(request.POST.get('divine_touch', 0))
#         sp_sav = float(request.POST.get('sp_sav', 0))
#         rss = float(request.POST.get('rss', 0))
#         loan_repay = float(request.POST.get('loan_repay', 0))
#         interest_repay = float(request.POST.get('interest_repay', 0))
#         commod_repay = float(request.POST.get('commod_repay', 0))
#         loan = float(request.POST.get('loan', 0))
#         interest = float(request.POST.get('interest', 0))
#         commod = float(request.POST.get('commod', 0))

#         # Update saving account fields
#         saving_account.received += received
#         saving_account.normal_savings += normal_savings
#         saving_account.divine_touch += divine_touch
#         saving_account.sp_sav += sp_sav
#         saving_account.rss += rss
#         saving_account.loan_repay += loan_repay
#         saving_account.interest_repay += interest_repay
#         saving_account.commod_repay += commod_repay
#         saving_account.loan += loan
#         saving_account.interest += interest
#         saving_account.commod += commod

#         saving_account.save()

#         messages.success(request, 'Saving account successfully updated or created.')
#         form = SavingDepositForm()  # Reset the form after saving
#     else:
#         form = SavingDepositForm()

#     return render(request, 'savings/savings_form.html', {'form': form, 'title': "Save"})


    
# def saving_deposit(request):
#     if request.method == 'POST':
#         owner_id = request.POST.get('owner')
#         payment_type = request.POST.get('payment_type')

#         try:
#             saving_account = SavingAccount.objects.get(owner_id=owner_id, payment_type=payment_type)
#         except SavingAccount.DoesNotExist:
#             saving_account = SavingAccount(owner_id=owner_id, payment_type=payment_type)

#         # Fetch values from the form, default to 0 if none provided
#         received = float(request.POST.get('received', 0))
#         normal_savings = float(request.POST.get('normal_savings', 0))
#         divine_touch = float(request.POST.get('divine_touch', 0))
#         sp_sav = float(request.POST.get('sp_sav', 0))
#         rss = float(request.POST.get('rss', 0))
#         loan_repay = float(request.POST.get('loan_repay', 0))
#         interest_repay = float(request.POST.get('interest_repay', 0))
#         commod_repay = float(request.POST.get('commod_repay', 0))
#         loan = float(request.POST.get('loan', 0))
#         interest = float(request.POST.get('interest', 0))
#         commod = float(request.POST.get('commod', 0))
#         share = float(request.POST.get('share', 0))  # Add share field

#         # Set the received value directly, without adding to the existing value
#         saving_account.received = received

#         # Update saving account fields
#         saving_account.normal_savings += normal_savings
#         saving_account.divine_touch += divine_touch
#         saving_account.sp_sav += sp_sav
#         saving_account.rss += rss
#         saving_account.loan_repay += loan_repay
#         saving_account.interest_repay += interest_repay
#         saving_account.commod_repay += commod_repay
#         saving_account.loan += loan
#         saving_account.interest += interest
#         saving_account.commod += commod
#         saving_account.share += share  # Update share

#         saving_account.save()

#         messages.success(request, 'Saving account successfully updated or created.')
#         form = SavingDepositForm()  # Reset the form after saving
#     else:
#         form = SavingDepositForm()

#     return render(request, 'savings/savings_form.html', {'form': form, 'title': "Save"})

# this is old version of the views

# def saving_deposit(request):
#     if request.method == 'POST':
#         owner_id = request.POST.get('owner')
#         payment_type = request.POST.get('payment_type')

#         try:
#             saving_account = SavingAccount.objects.get(owner_id=owner_id, payment_type=payment_type)
#         except SavingAccount.DoesNotExist:
#             saving_account = SavingAccount(owner_id=owner_id, payment_type=payment_type)

#         # Fetch values from the form, default to 0 if none provided
#         received = float(request.POST.get('received', 0))
#         normal_savings = float(request.POST.get('normal_savings', 0))
#         divine_touch = float(request.POST.get('divine_touch', 0))
#         sp_sav = float(request.POST.get('sp_sav', 0))
#         rss = float(request.POST.get('rss', 0))
#         loan_repay = float(request.POST.get('loan_repay', 0))
#         interest_repay = float(request.POST.get('interest_repay', 0))
#         commod_repay = float(request.POST.get('commod_repay', 0))
#         loan = float(request.POST.get('loan', 0))
#         interest = float(request.POST.get('interest', 0))
#         commod = float(request.POST.get('commod', 0))

#         # Update saving account fields
#         saving_account.received += received
#         saving_account.normal_savings += normal_savings
#         saving_account.divine_touch += divine_touch
#         saving_account.sp_sav += sp_sav
#         saving_account.rss += rss
#         saving_account.loan_repay += loan_repay
#         saving_account.interest_repay += interest_repay
#         saving_account.commod_repay += commod_repay
#         saving_account.loan += loan
#         saving_account.interest += interest
#         saving_account.commod += commod

#         saving_account.save()

#         messages.success(request, 'Saving account successfully updated or created.')
#         form = SavingDepositForm()  # Reset the form after saving
#     else:
#         form = SavingDepositForm()

#     return render(request, 'savings/savings_form.html', {'form': form, 'title': "Save"})


import logging

logger = logging.getLogger(__name__)

def saving_deposit(request):
    saving_account = None

    if request.method == 'POST':
        owner_id = request.POST.get('owner')
        
        if not owner_id:
            messages.error(request, 'No owner selected.')
            return redirect('savings:saving_deposit')

        # Get or create a new SavingAccount
        saving_account, created = SavingAccount.objects.get_or_create(owner_id=owner_id)
        if created:
            messages.success(request, 'New saving account created for the selected owner.')

        # Process form data
        form = SavingDepositForm(request.POST, instance=saving_account)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Set 'received' directly
            saving_account.received = int(request.POST.get('received', '0').replace(',', '').strip() or 0)

            # Update balance fields using add/subtract fields
            saving_account.savings_balance = cleaned_data['savings_balance']
            saving_account.divine_touch_balance = cleaned_data['divine_touch_balance']
            saving_account.rss_balance = cleaned_data['rss_balance']
            saving_account.share_balance = cleaned_data['share_balance']

            # Store the last entered values for the add/subtract fields
            # Update main fields based on add/subtract inputs without accumulating
            if cleaned_data.get('add_savings') or cleaned_data.get('subtract_savings'):
                saving_account.savings = cleaned_data.get('add_savings', 0) - cleaned_data.get('subtract_savings', 0)

            if cleaned_data.get('add_divine_touch') or cleaned_data.get('subtract_divine_touch'):
                saving_account.divine_touch = cleaned_data.get('add_divine_touch', 0) - cleaned_data.get('subtract_divine_touch', 0)

            if cleaned_data.get('add_rss') or cleaned_data.get('subtract_rss'):
                saving_account.rss = cleaned_data.get('add_rss', 0) - cleaned_data.get('subtract_rss', 0)

            if cleaned_data.get('add_share') or cleaned_data.get('subtract_share'):
                saving_account.share = cleaned_data.get('add_share', 0) - cleaned_data.get('subtract_share', 0)

            # Update loan, interest, and commodity balances based on repayment fields
            saving_account.loan_balance = max(
                0, saving_account.loan_balance + cleaned_data.get('loan', 0) - cleaned_data.get('loan_repay', 0)
            )
            saving_account.interest_balance = max(
                0, saving_account.interest_balance + cleaned_data.get('interest', 0) - cleaned_data.get('interest_repay', 0)
            )
            saving_account.commodity_balance = max(
                0, saving_account.commodity_balance + cleaned_data.get('commod', 0) - cleaned_data.get('commod_repay', 0)
            )
            
            saving_account.save()
            messages.success(request, 'Saving account successfully updated.')
            form = SavingDepositForm()  # Clear the form after saving
        else:
            print(form.errors)  # Add this line to log errors
            messages.error(request, 'There were errors in the form. Please correct them.')
    else:
        form = SavingDepositForm()

    return render(request, 'savings/savings_form.html', {'form': form, 'title': "Save"})



def edit_saving_account(request):
    saving_account = None

    if 'owner' in request.GET and 'month' in request.GET and 'year' in request.GET:
        owner = request.GET.get('owner')
        month = request.GET.get('month')
        year = request.GET.get('year')

        # Get the existing saving account instance
        saving_account = get_object_or_404(SavingAccount, owner_id=owner, month=month, year=year)

    if request.method == 'POST':
        form = SavingAccountEditForm(request.POST, instance=saving_account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saving account successfully updated.')
            return redirect('savings:edit_saving_account')  # Redirect to avoid resubmission
    else:
        form = SavingAccountEditForm(instance=saving_account)

    return render(request, 'savings/edit_saving_account.html', {'form': form, 'title': "Edit Saving Account"})

from django.urls import reverse
from django.http import HttpResponseNotAllowed

def delete_transaction(request, pk):
    transaction = get_object_or_404(SavingAccount, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction record successfully deleted.')
        return redirect(reverse('savings:transaction_list'))  # Update 'savings:transaction_list' with your redirect path

    elif request.method == 'GET':
        # Display the confirmation page
        return render(request, 'savings/transaction_confirm_delete.html', {'transaction': transaction})
    
    # Reject other HTTP methods
    return HttpResponseNotAllowed(['POST', 'GET'])



def saving_withdrawal(request, **kwargs):
    template = 'savings/savings_form.html'

    if request.method == "POST":
        form = SavingWithdrawalForm(request.POST)
        if form.is_valid():
            withdraw = form.save(commit=False)
            if withdraw.account.status == 'Deactivated':
                messages.warning(request,
                        "This account is not yet activated please activate the account first")
                return redirect("savings:saving")
            # checks if withdrawal amount is valid
            if(withdraw.account.current_balance >= withdraw.amount and
                    withdraw.amount >= 10):
                withdraw.account.current_balance -= withdraw.amount
                withdraw.account.save()
                withdraw.save()
                messages.success(
                    request,
                    'You Have Withdrawn Rs. {} only from the account number {}.'
                    .format(withdraw.amount,withdraw.account.owner.mem_number))

                if 'pk' in kwargs:
                    return redirect("savings:withdrawpk", pk=kwargs['pk'])
                return redirect("savings:withdraw")
            else:
                messages.error(
                    request,
                    "Either you are trying to withdraw Rs. less than 10 or your current balance is not sufficient"
                )
    else:
        if 'pk' in kwargs:
            ac = kwargs['pk']
            form = SavingWithdrawalForm()
            form.fields["account"].queryset = SavingAccount.objects.filter(id=ac)
            form.fields["account"].initial = ac
            form.fields["account"].widget = forms.HiddenInput() 
        else:
            form = SavingWithdrawalForm()

    context = {
        'form': form,
        'title': "Withdraw"
    }

    return render(request, template, context)



from django.db.models import Sum

def saving_deposit_transactions(request):
    template = 'savings/savings_transactions.html'
    savings = SavingAccount.objects.filter(owner__is_staff=False, owner__is_superuser=False)
    sorted_savings = savings.order_by('owner__last_name', 'owner__first_name')
    savings_sum = savings.aggregate(Sum('received'))['received__sum'] or 0

    context = {
        'transactions': sorted_savings,
        'transactions_sum': savings_sum,
        'title': "Deposit Transactions",
    }

    return render(request, template, context)




def teller_savings_transactions(request):
    template = 'savings/teller_savings_transactions.html'

    # Fetch all saving accounts with a payment_type of "Teller"
    teller_savings = SavingAccount.objects.filter(payment_type='Teller')

    # Aggregate the total received amount for Teller savings
    teller_savings_sum = teller_savings.aggregate(Sum('received'))['received__sum']

    # Sort transactions by owner's last name and first name
    sorted_teller_savings = teller_savings.order_by('owner__last_name', 'owner__first_name')

    context = {
        'transactions': sorted_teller_savings,
        'transactions_sum': teller_savings_sum,
        'title': "Teller Savings",
    }

    return render(request, template, context)


def oracle_savings_transactions(request):
    template = 'savings/oracle_savings_transactions.html'

    # Fetch all saving accounts with a payment_type of "Oracle"
    oracle_savings = SavingAccount.objects.filter(payment_type='Oracle')

    # Aggregate the total received amount for Oracle savings
    oracle_savings_sum = oracle_savings.aggregate(Sum('received'))['received__sum']

    # Sort transactions by owner's last name and first name
    sorted_oracle_savings = oracle_savings.order_by('owner__last_name', 'owner__first_name')

    context = {
        'transactions': sorted_oracle_savings,
        'transactions_sum': oracle_savings_sum,
        'title': "Oracle Savings",
    }

    return render(request, template, context)



def generate_excel_savings(savings, filename):
    """
    Generates an Excel file from the provided savings queryset.
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Savings Records'

    headers = [
        'Month',
        'Owner',
        'Received',
        'Savings',
        'Divine Touch',
        'RSS',
        'Shares',
        'Loan',
        'Interest',
        'Commodity',
        'Savings Balance',
        'Divine Touch Balance',
        'Shares Balance',
        'Rss Balance',
        'Loan Balance',
        'Interest Balance',
        'Commodity Balance'
    ]
    sheet.append(headers)

    for saving in savings:
        sheet.append([
            saving.get_month_display(),
            f"{saving.owner.first_name} {saving.owner.last_name}",
            saving.received,
            saving.savings,
            saving.divine_touch,
            saving.rss,
            savings.share,
            saving.loan,
            saving.interest,
            saving.commod,
            savings.savings_balance,
            savings.divine_touch_balance,
            savings.share_balance,
            savings.rss_balance,
            savings.loan_balance,
            savings.interest_balance,
            savings.commodity_balance
        ])

    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                cell_length = len(str(cell.value))
                if cell_length > max_length:
                    max_length = cell_length
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column_letter].width = adjusted_width

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    return response

def generate_pdf_savings(savings, filename):
    """
    Generates a PDF file from the provided savings queryset.
    """
    template = get_template('savings/savings_transactions.html')
    context = {'transactions': savings}
    html_content = template.render(context)

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}.pdf'
    return response

@login_required
def download_all_savings_excel(request):
    savings = SavingAccount.objects.filter(
        owner__is_staff=False,
        owner__is_superuser=False
    ).order_by('owner__last_name', 'owner__first_name')
    return generate_excel_savings(savings, 'All_Savings')

@login_required
def download_all_savings_pdf(request):
    savings = SavingAccount.objects.filter(
        owner__is_staff=False,
        owner__is_superuser=False
    ).order_by('owner__last_name', 'owner__first_name')
    return generate_pdf_savings(savings, 'All_Savings')

@login_required
def download_teller_savings_excel(request):
    teller_savings = SavingAccount.objects.filter(
        payment_type='Teller'
    ).order_by('owner__last_name', 'owner__first_name')
    return generate_excel_savings(teller_savings, 'Teller_Savings')

@login_required
def download_teller_savings_pdf(request):
    teller_savings = SavingAccount.objects.filter(
        payment_type='Teller'
    ).order_by('owner__last_name', 'owner__first_name')
    return generate_pdf_savings(teller_savings, 'Teller_Savings')

@login_required
def download_oracle_savings_excel(request):
    oracle_savings = SavingAccount.objects.filter(
        payment_type='Oracle'
    ).order_by('owner__last_name', 'owner__first_name')
    return generate_excel_savings(oracle_savings, 'Oracle_Savings')

@login_required
def download_oracle_savings_pdf(request):
    oracle_savings = SavingAccount.objects.filter(
        payment_type='Oracle'
    ).order_by('owner__last_name', 'owner__first_name')
    return generate_pdf_savings(oracle_savings, 'Oracle_Savings')




def saving_withdrawal_transactions(request):
    template = 'savings/savings_transactions.html'

    savings = SavingWithdrawal.objects.filter(delete_status=False)
    savings_sum = savings.aggregate(Sum('amount'))['amount__sum']

    context = {
        'transactions': savings,
        'transactions_sum': savings_sum,
        'title': "Withdrawal",
    }

    return render(request, template, context)

def get_saving_account(request):
    template = 'savings/savings_form.html'

    form = GetSavingAccountForm(request.POST or None)

    if form.is_valid():
        savings_account = form.save(commit=False)
        pk = savings_account.account.pk
        request.session['ordered_savings_pk']=pk
        return redirect("savings:de|activate")

    context = {
        'form': form,
        'title': "de|activate",
    }

    return render(request, template, context)


def saving_deposit_transaction(request):
    template = 'savings/savings_transactions.html'

    # Fetch all saving accounts (regardless of payment_type)
    savings = SavingAccount.objects.filter(owner__is_staff=False, owner__is_superuser=False)

    # Aggregate the total received amount across all accounts
    savings_sum = savings.aggregate(Sum('received'))['received__sum']

    # Combine received amounts for users with both Teller and Oracle records
    combined_savings = {}
    for saving in savings:
        key = saving.owner_id
        if key not in combined_savings:
            combined_savings[key] = {
                'owner': saving.owner,
                'normal_savings': saving.normal_savings,
                'balance': saving.balance,
                'loan': saving.loan,
                'loan_balance': saving.loan_balance,
                'divine_touch': saving.divine_touch,
                'sp_sav': saving.sp_sav,
                'rss': saving.rss,
                'loan_repay': saving.loan_repay,
                'interest': saving.interest,
                'commod': saving.commod,
                'teller_received': 0,
                'oracle_received': 0,
                'payment_type': saving.payment_type
            }
        
        # Add received based on the payment type
        if saving.payment_type == 'Teller':
            combined_savings[key]['teller_received'] = saving.received
        elif saving.payment_type == 'Oracle':
            combined_savings[key]['oracle_received'] = saving.received
    
    # Prepare the final combined transactions with a flag to indicate whether it's a sum
    for key, data in combined_savings.items():
        data['received'] = data['teller_received'] + data['oracle_received']
        data['has_oracle_savings'] = data['oracle_received'] > 0
        data['has_teller_savings'] = data['teller_received'] > 0
        data['is_sum'] = data['has_oracle_savings'] and data['has_teller_savings']

    context = {
        'transactions': combined_savings.values(),
        'transactions_sum': savings_sum,
        'title': "Deposit",
    }

    return render(request, template, context)


def generate_pdf(request):
    # Fetch all saving accounts (you can add other filters if needed)
    saving_accounts = SavingAccount.objects.all()

    # Calculate total savings sum
    total_savings_sum = saving_accounts.aggregate(Sum('savings'))['savings__sum']

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="savings_deposit_report.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    p.setTitle("Savings Deposit Report")

    # Draw text on the PDF
    p.drawString(100, 750, "Savings Deposit Report")
    p.drawString(100, 730, f"Total Savings: {total_savings_sum}")

    # Draw the transactions
    height = 700
    for account in saving_accounts:
        p.drawString(100, height, f"Owner: {account.owner.first_name} {account.owner.last_name}")
        p.drawString(100, height-20, f"Savings: {account.savings}, Divine Touch: {account.divine_touch}, SP SAV: {account.sp_sav}")
        p.drawString(100, height-40, f"RSS: {account.rss}, Loan Repay: {account.loan_repay}, Interest: {account.interest}, Commod: {account.commod}")
        height -= 60  # Adjust the height as needed

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def saving_withdrawal_transaction(request):
    template = 'savings/savings_transactions.html'

    form = GetSavingAccountForm(request.POST or None)

    if form.is_valid():
        ordered_account = form.save(commit=False)
        savings = SavingWithdrawal.objects.filter(account = ordered_account.account, delete_status=False)
        savings_sum = savings.aggregate(Sum('amount'))['amount__sum']
        messages.success(request,
                         'Withdrawal ransactions of savings account number {}.'
                         .format(ordered_account.account.owner.mem_number))

        context = {
            'transactions':savings,
            'transactions_sum':savings_sum,
            'title': "Withdrawal",
        }

        return render(request, template, context)
    context = {
        'form':form,
        'title': "Withdrawal",
    }

    return render(request, template, context)

def saving(request):
    template = 'savings/savings.html'

    return render(request, template)

def saving_deposit_delete(request, pk):
    template = 'savings/savings_delete.html'

    deposit = get_object_or_404(SavingDeposit, pk=pk)

    if request.method == "POST":
        deposit.account.current_balance -= deposit.amount
        deposit.account.save()
        deposit.delete_status = True
        deposit.save()
        messages.success(request,
                        'You successfully deleted saving_deposit of account {} and amount {}.'
                        .format(deposit.account,deposit.amount))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': deposit,
        'type': "deposit",
    }

    return render(request, template, context)

def saving_withdrawal_delete(request, pk):
    template = 'savings/savings_delete.html'

    withdrawal = get_object_or_404(SavingWithdrawal, pk=pk)

    if request.method == "POST":
        withdrawal.account.current_balance += withdrawal.amount
        withdrawal.account.save()
        withdrawal.delete_status = True
        withdrawal.save()
        messages.success(request,
                        'You successfully deleted saving_withdrawal of account {} and amount {}.'
                        .format(withdrawal.account,withdrawal.amount))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': withdrawal,
        'type': "withdrawal",
    }

    return render(request, template, context)


def monthly_savings_report(request, month, year):
    template = 'savings/monthly_savings_report.html'

    # Fetch all saving accounts for the specified month and year
    monthly_savings = SavingAccount.objects.filter(month=month, year=year)

    # Aggregate the total received amount for the month, grouped by owner
    monthly_savings_sum = monthly_savings.aggregate(Sum('received'))['received__sum']

    # Dictionary to combine savings for each user
    combined_savings = {}
    
    for saving in monthly_savings:
        key = saving.owner_id
        
        # Check if the user already exists in combined_savings
        if key not in combined_savings:
            # Create a combined entry for the user
            combined_savings[key] = {
                'owner': saving.owner,
                'savings': saving.savings,
                'divine_touch': saving.divine_touch,
                'sp_sav': saving.sp_sav,
                'rss': saving.rss,
                'loan_repay': saving.loan_repay,
                'interest': saving.interest,
                'commod': saving.commod,
                'received': saving.received,
                'received_source': {saving.source}  # Store source in a set for uniqueness
            }
        else:
            # If the user already exists, add up the values and sources
            combined_savings[key]['received'] += saving.received
            combined_savings[key]['received_source'].add(saving.source)  # Add new source
            
    # Convert the set to a list for easy handling in the template
    for key in combined_savings:
        combined_savings[key]['received_source'] = list(combined_savings[key]['received_source'])

    # Context passed to the template
    context = {
        'transactions': combined_savings.values(),
        'transactions_sum': monthly_savings_sum,
        'month': month,
        'year': year,
        'title': f"Savings Report for {month}/{year}",
    }

    return render(request, template, context)



def yearly_savings_report(request, year):
    template = 'savings/yearly_savings_report.html'

    # Fetch all saving accounts for the specified year
    yearly_savings = SavingAccount.objects.filter(year=year)

    # Aggregate the total received amount for the year
    yearly_savings_sum = yearly_savings.aggregate(Sum('received'))['received__sum']

    # Combine received amounts for users with both Teller and Oracle records
    combined_savings = {}
    for saving in yearly_savings:
        key = saving.owner_id
        if key not in combined_savings:
            combined_savings[key] = saving
        else:
            combined_savings[key].received += saving.received

    context = {
        'transactions': combined_savings.values(),
        'transactions_sum': yearly_savings_sum,
        'year': year,
        'title': f"Savings Report for {year}",
    }

    return render(request, template, context)


def add_loan_account(request):
    if request.method == 'POST':
        form = LoanAccountForm(request.POST)
        if form.is_valid():
            loan_account = form.save(commit=False)
            loan_account.save()
            messages.success(request, 'Loan account successfully updated or created.')
    else:
        form = LoanAccountForm()
    return render(request, 'savings/loan_account_form.html', {'form': form, 'title': "Add Loan Account"})


def add_interest_account(request):
    if request.method == 'POST':
        form = InterestAccountForm(request.POST)
        if form.is_valid():
            interest_account = form.save(commit=False)
            interest_account.save()
            messages.success(request, 'Interest account successfully updated or created.')
    else:
        form = InterestAccountForm()
    return render(request, 'savings/interest_account_form.html', {'form': form, 'title': "Add Interest Account"})


def add_commodity_account(request):
    if request.method == 'POST':
        form = CommodityAccountForm(request.POST)
        if form.is_valid():
            commodity_account = form.save(commit=False)
            commodity_account.save()
            messages.success(request, 'Commodity account successfully updated or created.')
    else:
        form = CommodityAccountForm()
    return render(request, 'savings/commodity_account_form.html', {'form': form, 'title': "Add Commodity Account"})

