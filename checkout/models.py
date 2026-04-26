from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="orders",
    )

    # Customer details
    full_name = models.CharField(max_length=100)
    email = models.EmailField()

    # Shipping details
    address1 = models.CharField(max_length=255, default="")
    address2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, default="")
    postal_code = models.CharField(max_length=20, default="")
    country = models.CharField(max_length=100, default="")

    # Payment + totals
    total = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_pid = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    # Link to actual product
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # Snapshot of price at time of purchase
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
