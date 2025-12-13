from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def product_list(request):
    return HttpResponse("Hello, this will be the product list page.")
