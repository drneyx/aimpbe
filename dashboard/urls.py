from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('regions/', RegionView.as_view(), name='regions'),
    path('district/', DistrictView.as_view(), name='district'),
]