from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your context data here
        context['title'] = 'Dashboard'
        context['data'] = {
            # Add any data you want to pass to the template
            'example_data': 'This is an example data.'
        }
        return context


class RegionView(View):
    def get(self, request):
        context = {}

        regions = Region.objects.all()
        form = RegionForm()
    
        context['region'] = regions
        context['form'] = form
       
        return render(request, 'settings/regions/regions.html', context)

    def post(self, request):
        form = RegionForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Region added successfully.')
            return JsonResponse({'status': 'success'}, status=200)

        else:
            messages.error(request, 'Error adding region.')
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    

    @method_decorator(csrf_exempt)
    def delete(self, request):
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            
            if not ids:
                return JsonResponse({'status': 'error', 'message': 'No IDs provided.'}, status=400)
            
            if isinstance(ids, int):
                ids = [ids]
            
            regions = Region.objects.filter(id__in=ids)
            deleted_count = regions.delete()[0]
            
            if deleted_count > 0:
                return JsonResponse({'status': 'success', 'deleted_count': deleted_count}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'No regions found to delete.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


class DistrictView(View):
    def get(self, request):
        context = {}

        regions = Region.objects.all()
        form = RegionForm()
    
        context['region'] = regions
        context['form'] = form
       
        return render(request, 'settings/regions/regions.html', context)

    def post(self, request):
        form = RegionForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Region added successfully.')
            return JsonResponse({'status': 'success'}, status=200)

        else:
            messages.error(request, 'Error adding region.')
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    

    @method_decorator(csrf_exempt)
    def delete(self, request):
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            
            if not ids:
                return JsonResponse({'status': 'error', 'message': 'No IDs provided.'}, status=400)
            
            if isinstance(ids, int):
                ids = [ids]
            
            regions = Region.objects.filter(id__in=ids)
            deleted_count = regions.delete()[0]
            
            if deleted_count > 0:
                return JsonResponse({'status': 'success', 'deleted_count': deleted_count}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'No regions found to delete.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)