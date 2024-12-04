from django.urls import path

from .views import (saving_deposit,saving_withdrawal,
        saving_deposit_transactions,saving_withdrawal_transactions,
        saving_deposit_transaction,saving_withdrawal_transaction,
        saving_account,saving,
        saving_deposit_delete,saving_withdrawal_delete,
        get_saving_account, teller_savings_transactions, 
        oracle_savings_transactions, monthly_savings_report, yearly_savings_report,
        generate_pdf, edit_saving_account, delete_transaction,
        download_all_savings_excel, download_all_savings_pdf, download_teller_savings_excel,
        download_teller_savings_pdf, download_oracle_savings_excel, download_oracle_savings_pdf,
        add_loan_account, add_interest_account, add_commodity_account)

app_name = 'savings'
urlpatterns = [
    path('', saving, name='saving'),
    path('get', get_saving_account, name='get_savings_account'),
    path('de|activate/', saving_account, name='de|activate'),
    path('deposit/', saving_deposit, name='deposit'),
    # path('deposit/<int:pk>/', saving_deposit, name='depositpk'),
    path('deposit/<int:pk>/delete/', saving_deposit_delete, name='deposit_delete'),
    path('withdraw/', saving_withdrawal, name='withdraw'),
    path('withdraw/<int:pk>/', saving_withdrawal, name='withdrawpk'),
    path('withdraw/<int:pk>/delete/', saving_withdrawal_delete, name='withdraw_delete'),
    path('deposit/transactions/', saving_deposit_transactions, name='transactions'),
    path('withdraw/transactions/', saving_withdrawal_transactions, name='withdraw_transactions'),
    path('deposit/transaction/', saving_deposit_transaction, name='transaction'),
    path('withdraw/transaction/', saving_withdrawal_transaction, name='withdraw_transaction'),
    path('teller-savings/', teller_savings_transactions, name='teller_savings_transactions'),
    path('oracle-savings/', oracle_savings_transactions, name='oracle_savings_transactions'),
    path('monthly/<int:month>/<int:year>/', monthly_savings_report, name='monthly'),
    path('yearly/<int:year>/', yearly_savings_report, name='yearly'),
    path('transactions/pdf/', generate_pdf, name='generate_pdf'),
    path('edit/', edit_saving_account, name='edit_saving_account'),
    path('delete/<int:pk>/', delete_transaction, name='delete_transaction'),
    # Download URLs for All Savings
    path('download/all/excel/', download_all_savings_excel, name='download_all_savings_excel'),
    path('download/all/pdf/', download_all_savings_pdf, name='download_all_savings_pdf'),

    # Download URLs for Teller Savings
    path('download/teller/excel/', download_teller_savings_excel, name='download_teller_savings_excel'),
    path('download/teller/pdf/', download_teller_savings_pdf, name='download_teller_savings_pdf'),

    # Download URLs for Oracle Savings
    path('download/oracle/excel/', download_oracle_savings_excel, name='download_oracle_savings_excel'),
    path('download/oracle/pdf/', download_oracle_savings_pdf, name='download_oracle_savings_pdf'),

    path('add-loan-account/', add_loan_account, name='add_loan_account'),
    path('add-interest-account/', add_interest_account, name='add_interest_account'),
    path('add-commodity-account/', add_commodity_account, name='add_commodity_account'),
    #path('download-template/', download_template, name='download_template'),
    #path('upload-savings/', upload_savings, name='upload_savings'),
]
