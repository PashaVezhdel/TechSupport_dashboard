from django.contrib import admin
from django.urls import path
from dashboard.views import test_db

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test_db),  
]