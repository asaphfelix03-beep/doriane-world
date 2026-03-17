from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("PREPARING", "En preparation"),
        ("SHIPPING", "En livraison"),
        ("DELIVERED", "Livree"),
    ]
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=160)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)
