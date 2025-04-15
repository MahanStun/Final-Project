from django.db import models
import datetime
from persiantools.jdatetime import JalaliDate as jmodels
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


# Create your models here.

from django.db import models
import datetime
# from persiantools.jdatetime import JalaliDate
from django.core.validators import FileExtensionValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    # states = ((1"Basic"),(2""),(3""))
    Product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, default=0, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="upload/cosmetics_picture/")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    # percent_show = models.IntegerField()

    def __str__(self):
        return self.Product_name
