from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from .models import NewsletterSubscription

# Safely register Site model only if not already registered
try:
    admin.site.register(Site, SiteAdmin)
except admin.sites.AlreadyRegistered:
    pass


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
