from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db.models import Q
from ..models import Product
from ..serializers import ProductSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.query_params.get('query', None)
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(district__name__icontains=query) |
                Q(region__name__icontains=query)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Products retrieved successfully",
            "data": serializer.data
        })