from django.contrib import admin
from django.urls import path

import reports.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/weekly/', reports.views.test)
]
