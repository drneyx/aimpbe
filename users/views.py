from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.views import View

class LoginView(TemplateView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Login'

        return context
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print('USERNAME', email)
        print('pass', password)

        user = authenticate(request, username=email, password=password)

        print('USER AUTH', user)

        if user is not None:
            login(request, user)

            if user.is_seller:
                return redirect(reverse_lazy('dashboard'))
        else:
            errors = {
                'email': 'Invalid email or password.',
                'password': 'Invalid email or password.'
            }
            return JsonResponse({'errors': errors}, status=400)


class RegisterView(TemplateView):
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Register'

        return context
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = SellerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login with your credentials.')
            return redirect(reverse_lazy('login') + '?registration_success=true' )
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'errors': errors}, status=400)


class SellerRegisterView(CreateView):
    model = CustomUser
    form_class = SellerRegistrationForm
    template_name = 'seller_register.html'
    success_url = reverse_lazy('seller-register-success')


class CustomerView(View):
    """
    Users management for all products
    """

    def get(self, request):
        customer_id = request.GET.get('id')
        context = {}

        if customer_id:
            customer = get_object_or_404(CustomUser, id=customer_id)
            # form = CategoryForm(instance=CustomUser)
            context['customer_obj'] = customer

        customers = CustomUser.objects.all()
        form = CustomerForm()
    
        context['customers'] = customers
        context['form'] = form
       
        return render(request, 'customers/customer.html', context)

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return JsonResponse({'status': 'success'}, status=200)

        else:
            messages.error(request, 'Error adding category.')
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)