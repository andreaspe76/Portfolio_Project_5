"""
Docstring for products.views
"""

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem

# Create your views here.


def get_cart(request):
    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
        if cart:
            return cart

    cart = Cart.objects.create()
    request.session["cart_id"] = cart.id
    return cart


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("product_detail", pk=pk)


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


def cart_detail(request):
    cart = get_cart(request)
    return render(request, "products/cart_detail.html", {
        "cart": cart
    })


def remove_from_cart(request, pk):
    cart = get_cart(request)
    item = CartItem.objects.filter(cart=cart, product_id=pk).first()

    if item:
        item.delete()

    return redirect("cart_detail")


def decrease_quantity(request, pk):
    cart = get_cart(request)
    item = CartItem.objects.filter(cart=cart, product_id=pk).first()

    if item:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect("cart_detail")
