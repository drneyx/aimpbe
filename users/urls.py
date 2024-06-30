from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', RegisterView.as_view(), name='forgot-password'),
    path('customers/', CustomerView.as_view(), name='customers'),

]