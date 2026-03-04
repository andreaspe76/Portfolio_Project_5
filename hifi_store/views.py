from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscription


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if NewsletterSubscription.objects.filter(email=email).exists():
            messages.warning(request, "This email is already subscribed.")
        else:
            NewsletterSubscription.objects.create(email=email)
            messages.success(
                request, "Thanks for subscribing to our newsletter!")

    return redirect('home')
