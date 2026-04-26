from django.conf import settings


def facebook_pixel(request):
    return {
        "FACEBOOK_PIXEL_ID": getattr(settings, "FACEBOOK_PIXEL_ID", "")
    }
