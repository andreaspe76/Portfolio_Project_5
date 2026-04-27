from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("success/<int:order_id>/",
         views.checkout_success, name="checkout_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("register/", views.register, name="register"),
]
