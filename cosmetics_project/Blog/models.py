from django.db import models
import datetime
from persiantools.jdatetime import JalaliDate as jmodels
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

from django.db import models
import datetime
# from persiantools.jdatetime import JalaliDate
from django.core.validators import FileExtensionValidator


# Create your models here.

class My_Blog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="upload/cosmetics_picture/")

    def __str__(self):
        return self.name

