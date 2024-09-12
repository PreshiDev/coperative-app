"""cooperative_finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import static_pages.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('static_pages/', include('static_pages.urls')),
    path('about/', static_pages.views.about, name="about"),
    path('contact/', static_pages.views.contact, name="contact"),
    path('savings/', include('savings.urls')),
    path('loans/', include('loans.urls')),
    path('shares/', include('shares.urls')),
    path('', include('members.urls')),
    path('reports/', include('reports.urls')),
    path('accounting/', include('accounting.urls')),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)