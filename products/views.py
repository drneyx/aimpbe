from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

class CategoryView(View):
    def get(self, request):
        category_id = request.GET.get('id')
        context = {}

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(instance=category)
            context['category'] = category

        categories = Category.objects.all()
        form = CategoryForm()
    
        context['categories'] = categories
        context['form'] = form
       
        return render(request, 'category/category_list.html', context)

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return JsonResponse({'status': 'success'}, status=200)

        else:
            messages.error(request, 'Error adding category.')
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
            
            categories = Category.objects.filter(id__in=ids)
            deleted_count = categories.delete()[0]
            
            if deleted_count > 0:
                return JsonResponse({'status': 'success', 'deleted_count': deleted_count}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'No categories found to delete.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
           
class CategoryDetailsView(View):
    def get(self, request, pk):
        context = {}
        category = get_object_or_404(Category, id=pk)
        context['category'] = category

        return render(request, 'category/category_details.html', context)

    def add_category(self, request):
        form = CategoryForm(request.POST, request.FILES)

        print(form.cleaned_data)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'status': 'success'}, status=200)
            messages.success(request, 'Category added successfully.')
        else:
            if request.is_ajax():
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Error adding category.')
        return redirect('category-list')

    def delete_category(self, request):
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category-list')

    def bulk_delete(self, request):
        ids = request.POST.getlist('category_ids')
        if ids:
            Category.objects.filter(id__in=ids).delete()
            messages.success(request, 'Selected categories deleted successfully.')
        else:
            messages.error(request, 'No categories selected for deletion.')
        return redirect('category-list')
    

class ProductView(View):
    """
    Product management for all products
    """

    def get(self, request):
        context = {}

        products = Product.objects.all()
        form = ProductForm()
    
        context['products'] = products
        context['form'] = form

        categories = Category.objects.all()
        context['categories'] = categories

        regions = Region.objects.all()
        context['regions'] = regions
       
        return render(request, 'products/products.html', context)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return JsonResponse({'status': 'success'}, status=200)

        else:
            messages.error(request, 'Error adding category.')
            print(form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        


class FetchDistrictsView(View):
    def get(self, request):
        region_id = request.GET.get('region_id')
        if region_id:
            districts = District.objects.filter(region_id=region_id).values('id', 'name')
            return JsonResponse(list(districts), safe=False)
        return JsonResponse({'error': 'Region ID not provided'}, status=400)