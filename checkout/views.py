import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    cart = request.session.get("cart", {})

    total = sum(
        item["price"] * item["quantity"]
        for item in cart.values()
    )

    total_cents = int(total * 100)

    if request.method == "POST":
        try:
            stripe.PaymentIntent.create(
                amount=total_cents,
                currency="eur",
            )
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
