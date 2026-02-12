from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("success/", views.checkout_success, name="checkout_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
