from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Product_dashboard

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_dashboard, on_delete=models.CASCADE)
    tracking_code = models.CharField(max_length=10, unique=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.tracking_code} for {self.user.username}"
