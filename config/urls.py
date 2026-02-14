from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_home, api_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_home, name='home'),
    path('api/data/', api_data, name='api_data'),
]