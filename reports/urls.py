from django.urls import path
from .views import report,income,expense,loan,capital,monthly,yearly
app_name = 'reports'
urlpatterns = [
    path('', report, name='reports'),
    path('income', income, name='income'),
    path('expense', expense, name='expense'),
    path('loans', loan, name='loan'),
    path('capital', capital, name='capital'),
        path('reports/monthly/', monthly, name='monthly'),
    path('reports/yearly/', yearly, name='yearly'),
]
