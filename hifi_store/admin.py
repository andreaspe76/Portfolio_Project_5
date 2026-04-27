from django.contrib import admin
from .models import NewsletterSubscription
from django.contrib.sites.models import Site

admin.site.register(Site)


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
