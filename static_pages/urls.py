from django.urls import path
from .views import home

app_name = 'static_pages'  # Optional: Namespace for the app's URLs

urlpatterns = [
    path('', home, name='home'),  # This will map the root of the dashboard to the home view
]
