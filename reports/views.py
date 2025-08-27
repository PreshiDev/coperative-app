from django.shortcuts import render, get_object_or_404, redirect
from accounting.models import Income,Expense
from loans.models import LoanPayment,LoanIssue,LoansIssue, LoanAccount
from shares.models import ShareBuy,ShareSell
from savings.models import SavingDeposit,SavingWithdrawal, SavingAccount
from django.db.models import Sum
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count

# import datetime

from reports.utils import generate_pdf, generate_excel  # Assume these utility functions are defined


# helper functions

def total_capital(keys, pre_context):
        for item in keys:
            if pre_context.get(item) != None:
                items_sum = 0
                items_sum = items_sum + pre_context[item]
                return items_sum

# Create your views here.

def report(request):
    template = 'reports/reports.html'

    return render(request, template)

def _income(year=datetime.now().year, month=datetime.now().month, yearly=False):
    if yearly == True:
        incomes = Income.objects.filter(delete_status = False, date_created__year = year)
    else:
        incomes = Income.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
    return incomes

def income(request):
    template = 'reports/income.html'

    # Implement date picker or something else that is less error prone
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        incomes = _income(year=year,month=month)
    else:
        incomes = _income()

    context = {
        'items_income': incomes,
        'title_income': 'Income',
        'total_income': incomes.aggregate(Sum('amount'))['amount__sum']
        }

    return render(request, template, context)

def _expense(year=datetime.now().year, month=datetime.now().month, yearly=False):
    if yearly == True:
        expenses = Expense.objects.filter(delete_status = False, date_created__year = year)
    else:
        expenses = Expense.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
    return expenses

def expense(request):
    template = 'reports/expense.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        expenses = _expense(year=year,month=month)
    else:
        expenses = _expense()

    context = {
            'items_expenses': _expense(),
            'title_expenses': "Expense",
            'total_expense': expenses.aggregate(Sum('amount'))['amount__sum']
            }

    return render(request, template, context)

def _loan(year=datetime.now().year, month=datetime.now().month, yearly=False):
    if yearly == True:
        loans_rec = LoanPayment.objects.filter(delete_status = False, date_created__year = year)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year)
    else:
        loans_rec = LoanPayment.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
    return {'loans_rec': loans_rec, 'loans_issued': loans_issued}

def loan(request):
    template = 'reports/loans.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        loan = _loan(year=year,month=month)
    else:
        loan = _loan()



    context = {
            'items_loans': loan.get("loans_rec","none"),
            'issued_items_loans': loan.get("loans_issued","none"),
            'title_loans': 'Loans',
            }

    return render(request, template, context)

def _capital(year=datetime.now().year, month=datetime.now().month,yearly=False):

    if yearly == True:
        shares_buy = ShareBuy.objects.filter(delete_status = False, date_created__year = year)
        shares_sell = ShareSell.objects.filter(delete_status = False, date_created__year = year)

        savings_deposit = SavingDeposit.objects.filter(delete_status = False, date_created__year = year)
        savings_withdrawal = SavingWithdrawal.objects.filter(delete_status = False, date_created__year = year)

        loan_payment = LoanPayment.objects.filter(delete_status = False, date_created__year = year)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year)
    else:
        shares_buy = ShareBuy.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        shares_sell = ShareSell.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)

        savings_deposit = SavingDeposit.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        savings_withdrawal = SavingWithdrawal.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)

        loan_payment = LoanPayment.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)

    shares_buy_sum = shares_buy.aggregate(Sum('number'))['number__sum']
    shares_sell_sum = shares_sell.aggregate(Sum('number'))['number__sum']

    savings_deposit_sum = savings_deposit.aggregate(Sum('amount'))['amount__sum']
    savings_withdrawal_sum= savings_withdrawal.aggregate(Sum('amount'))['amount__sum']

    loan_payment_sum= loan_payment.aggregate(Sum('principal'))['principal__sum']
    loans_issued_sum = loans_issued.aggregate(Sum('principal'))['principal__sum']

    return {'shares_buy_sum': shares_buy_sum, 'shares_sell_sum': shares_sell_sum,
	'savings_deposit_sum': savings_deposit_sum, 'savings_withdrawal_sum':savings_withdrawal_sum,
	'loan_payment_sum': loan_payment_sum,'loans_issued_sum': loans_issued_sum,
  	 }



def capital(request):
    template = 'reports/capital.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        capital = _capital(year=year,month=month)
    else:
        capital = _capital()

    pre_context = {
                0: capital.get('shares_buy_sum'),
                1: capital.get('savings_deposit_sum'),
                2: capital.get('loan_payment_sum'),
                3: capital.get('shares_sell_sum'),
                4: capital.get('savings_withdrawal_sum'),
                5: capital.get('loans_issued_sum'),
                }

    context = {
            'shares_buy_sum_capital': pre_context[0],
            'savings_deposit_sum_capital': pre_context[1],
            'loan_payment_sum_capital': pre_context[2],
            'shares_sell_sum_capital': pre_context[3],
            'savings_withdrawal_sum_capital': pre_context[4],
            'loans_issued_sum_capital': pre_context[5],
            'total_capital_additions': total_capital([0,1,2], pre_context),
            'total_capital_deductions': total_capital([3,4,5], pre_context),
            'title_capital': 'Capital',
            }

    return render (request, template, context)


def monthly(request):
    template = 'reports/monthly.html'

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Generate month choices using datetime to format month names correctly
    MONTH_CHOICES = [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    # Generate year choices
    YEAR_CHOICES = [(year, year) for year in range(current_year - 20, current_year + 1)]

    if request.method == 'POST':
        selected_month = int(request.POST.get('month', current_month))
        selected_year = int(request.POST.get('year', current_year))
    else:
        selected_month = current_month
        selected_year = current_year

    # Query filtering for savings
    savings = SavingAccount.objects.filter(month=selected_month, year=selected_year)

    # Handle PDF and Excel file generation
    if 'download_pdf' in request.POST:
        pdf_content = generate_pdf(savings)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=Monthly_Report_{selected_month}_{selected_year}.pdf'
        return response

    if 'download_excel' in request.POST:
        excel_content = generate_excel(savings)
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Monthly_Report_{selected_month}_{selected_year}.xlsx'
        return response

    context = {
        'savings': savings,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'title': 'Monthly Report',
        'MONTH_CHOICES': MONTH_CHOICES,
        'YEAR_CHOICES': YEAR_CHOICES,
    }

    return render(request, template, context)


def yearly(request):
    template = 'reports/yearly.html'

    # Get the current year
    current_year = datetime.now().year

    # Generate year choices
    YEAR_CHOICES = [(year, year) for year in range(current_year - 20, current_year + 1)]

    if request.method == 'POST':
        selected_year = int(request.POST.get('year', current_year))
    else:
        selected_year = current_year

    # Query filtering for savings
    savings = SavingAccount.objects.filter(year=selected_year)

    # Handle PDF and Excel file generation
    if 'download_pdf' in request.POST:
        pdf_content = generate_pdf(savings)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=Yearly_Report_{selected_year}.pdf'
        return response

    if 'download_excel' in request.POST:
        excel_content = generate_excel(savings)
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Yearly_Report_{selected_year}.xlsx'
        return response

    context = {
        'savings': savings,
        'selected_year': selected_year,
        'title': 'Yearly Report',
        'YEAR_CHOICES': YEAR_CHOICES,
    }

    return render(request, template, context)

# This view below is the previous view that uses HttpResponseForbidden to display error message which works, but i do not want to use messages to display success message anymore

# def delete_transaction(request, transaction_id):
#     if request.method == 'POST':
#         # Fetch the transaction record or return 404 if it doesn't exist
#         transaction = get_object_or_404(SavingAccount, pk=transaction_id)
        
#         # Verify that the user has the required permission to delete a transaction
#         if not request.user.has_perm('savings.delete_savingaccount'):
#             return HttpResponseForbidden("You don't have permission to delete this record.")
        
#         # Delete the transaction only
#         transaction.delete()
#         messages.success(request, 'Record deleted successfully.')

#         # Redirect to the monthly report page
#         return redirect('reports:monthly')
    
#     return HttpResponseForbidden("Invalid request method.")


def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        # Fetch the transaction record or return 404 if it doesn't exist
        transaction = get_object_or_404(SavingAccount, pk=transaction_id)
        
        # Verify that the user has the required permission to delete a transaction
        if not request.user.has_perm('savings.delete_savingaccount'):
            return HttpResponse("You don't have permission to delete this record.", status=403)
        
        # Delete the transaction only
        transaction.delete()
        
        # Return an HttpResponse with the success message
        return HttpResponse("Record deleted successfully.")
    
    return HttpResponse("Invalid request method.", status=403)



@login_required
@permission_required('savings.delete_savingaccount', raise_exception=True)
def bulk_delete_records(request):
    template = 'reports/bulk_delete.html'
    
    # Get all months/years that have records
    months_with_records = SavingAccount.objects.values('month', 'year').annotate(
        record_count=Count('id')
    ).order_by('-year', '-month')
    
    # Get unique years
    years = SavingAccount.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Format month names for display
    formatted_records = []
    for record in months_with_records:
        month_num = record['month']
        year = record['year']
        month_name = datetime(2000, month_num, 1).strftime('%B')
        formatted_records.append({
            'month': month_num,
            'year': year,
            'month_name': month_name,
            'record_count': record['record_count']
        })
    
    context = {
        'months_with_records': formatted_records,
        'years': years,
        'title': 'Bulk Record Deletion'
    }
    
    return render(request, template, context)

@login_required
@permission_required('savings.delete_savingaccount', raise_exception=True)
def delete_month_records(request, month, year):
    if request.method == 'POST':
        # Verify the user confirmed the deletion
        if 'confirm_delete' not in request.POST:
            return JsonResponse({
                'success': False,
                'message': "Deletion not confirmed."
            }, status=400)
        
        # Get all records for the specified month and year
        records_to_delete = SavingAccount.objects.filter(month=month, year=year)
        record_count = records_to_delete.count()
        
        # Delete the records
        records_to_delete.delete()
        
        return JsonResponse({
            'success': True,
            'message': f"Successfully deleted {record_count} records for {datetime(2000, month, 1).strftime('%B')} {year}."
        })
    
    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    }, status=400)

@login_required
@permission_required('savings.delete_savingaccount', raise_exception=True)
def delete_year_records(request, year):
    if request.method == 'POST':
        # Verify the user confirmed the deletion
        if 'confirm_delete' not in request.POST:
            return JsonResponse({
                'success': False,
                'message': "Deletion not confirmed."
            }, status=400)
        
        # Get all records for the specified year
        records_to_delete = SavingAccount.objects.filter(year=year)
        record_count = records_to_delete.count()
        
        # Delete the records
        records_to_delete.delete()
        
        return JsonResponse({
            'success': True,
            'message': f"Successfully deleted {record_count} records for the year {year}."
        })
    
    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    }, status=400)