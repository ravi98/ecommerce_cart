from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, LoginSerializer
from .models import Product, Category
from cart.forms import CartAddProductForm

from rest_framework.views import APIView

# Create your views here.

#view to list products based on categories

class UserRegistration(APIView):
    # @api_view(['GET', 'POST'])
    serializer_class=UserSerializer
    
    def post(self, request):
        if request.method=="POST":
            data=request.data
            srzd_data=UserSerializer(data=data)
            if srzd_data.is_valid(raise_exception=True):
                srzd_data.save()
                return redirect('social:user_login')
class UserLogin(APIView):
    serializer_class=LoginSerializer
    
    def post(self, request):
        if request.method=="POST":
            data=request.data
            srzd_data=LoginSerializer(data=data)
            if srzd_data.is_valid(raise_exception=True):
                login(request, srzd_data.validated_data.get('user'))
            return redirect('social:product_list')


def custom_logout(request):
    logout(request)
    return redirect('social:user_login')


def product_list(request, category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.all()
    if category_slug:
        category=get_object_or_404(Category, slug=category_slug)
        products=products.filter(category=category)
        print()
    return render(
        request,
        'social/products/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )

def product_details(request, id, slug):
    product=get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )
    cart_product_form=CartAddProductForm()
    
    return render(
        request,
        'social/products/detail.html',
        {
            'product':product,
            'cart_product_form':cart_product_form
        }
    )


    