from django.urls import path
from .views import (report,income,expense,loan,capital,
monthly,yearly,delete_transaction, bulk_delete_records, 
delete_month_records, delete_year_records)
app_name = 'reports'
urlpatterns = [
    path('', report, name='reports'),
    path('income', income, name='income'),
    path('expense', expense, name='expense'),
    path('loans', loan, name='loan'),
    path('capital', capital, name='capital'),
    path('reports/monthly/', monthly, name='monthly'),
    path('reports/yearly/', yearly, name='yearly'),
    path('delete_transaction/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
        path('bulk-delete/', bulk_delete_records, name='bulk_delete_records'),
    path('delete-month/<int:month>/<int:year>/', delete_month_records, name='delete_month_records'),
    path('delete-year/<int:year>/', delete_year_records, name='delete_year_records'),
]
