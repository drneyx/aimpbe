from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('categories/<pk>/details/', CategoryDetailsView.as_view(), name='category-details'),
    path('products/', ProductView.as_view(), name='products'),
     path('fetch-districts/', FetchDistrictsView.as_view(), name='fetch-districts'),
]
