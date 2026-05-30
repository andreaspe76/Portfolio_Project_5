from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import ProfileForm
from django.contrib import messages
from django.contrib.auth import logout


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("edit_profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def delete_profile(request):
    user = request.user  # FIX: you forgot to define 'user'

    if request.method == "POST":
        # Delete the profile if it exists
        UserProfile.objects.filter(user=user).delete()

        # Delete the user account itself
        user.delete()

        # Log out the session
        logout(request)

        messages.success(request, "Your account has been deleted.")
        return redirect("home")  # or your homepage URL name

    return render(request, "accounts/delete_profile.html")
