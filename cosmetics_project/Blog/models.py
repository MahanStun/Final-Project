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


class My_Blog(models.Model):
    # states = ((1"Basic"),(2""),(3""))
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

