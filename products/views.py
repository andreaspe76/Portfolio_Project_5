from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def product_list(request):
    products = Product.objects.all()
    template = "products/product_list.html"
    if request.user_agent.is_mobile:
        template = "products/product_list_mobile.html"

    return render(request, template, {
        "products": products
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    template = "products/product_detail.html"
    if request.user_agent.is_mobile:
        template = "products/product_detail_mobile.html"

    return render(request, template, {
        "product": product

    })
