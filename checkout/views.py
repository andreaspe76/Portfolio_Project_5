import stripe
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from products.models import Cart
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    # Get the latest cart (submission-safe approach)
    cart = Cart.objects.last()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("products")

    # Calculate total from CartItems
    total = Decimal("0.00")

    for item in cart.items.all():
        total += item.product.price * item.quantity

    total_cents = int(total * 100)

    if request.method == "POST":
        try:
            stripe.PaymentIntent.create(
                amount=total_cents,
                currency="eur",
            )

            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=request.POST.get("full_name", "Guest"),
                email=request.POST.get("email", "guest@example.com"),
                total=total,
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )

            # Clear cart after successful checkout
            cart.delete()

            return redirect("checkout_success")

        except stripe.error.CardError:
            messages.error(request, "Your card was declined.")

    context = {
        "cart": cart,
        "total": total,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, "checkout/checkout.html", context)


def checkout_success(request):
    return render(request, "checkout/checkout_success.html")
