from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import ProfileForm
from django.contrib import messages


@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("edit_profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def delete_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        profile.delete()
        messages.success(request, "Your profile has been deleted.")
        return redirect("edit_profile")  # or redirect to homepage

    return render(request, "accounts/delete_profile.html", {"profile": profile})
