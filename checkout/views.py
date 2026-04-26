from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import stripe
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from products.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    # Get the latest cart for the session
    cart_id = request.session.get("cart_id")
    cart = Cart.objects.filter(id=cart_id).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("products_list")

    # Calculate total from CartItems
    total = Decimal("0.00")
    for item in cart.items.all():
        total += item.product.price * item.quantity

    total_cents = int(total * 100)

    form = CheckoutForm()

    intent = stripe.PaymentIntent.create(
        amount=total_cents,
        currency="eur",
    )

    # Handle POST request for checkout form submission
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():

            # Create a fresh PaymentIntent for POST
            intent = stripe.PaymentIntent.create(
                amount=total_cents,
                currency="eur",
            )

            # Create order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                address1=form.cleaned_data["address1"],
                address2=form.cleaned_data["address2"],
                city=form.cleaned_data["city"],
                postal_code=form.cleaned_data["postal_code"],
                country=form.cleaned_data["country"],
                total=total,
                stripe_pid=intent.id,
            )

            # Create order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )

            # Clear cart after successful checkout
            cart.delete()
            request.session["cart_id"] = None

            return redirect("checkout_success", order_id=order.id)

    # Render checkout page
    context = {
        "cart": cart,
        "total": total,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "form": form,
        "client_secret": intent.client_secret,
    }

    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "checkout/checkout_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "checkout/my_orders.html", {"orders": orders})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
