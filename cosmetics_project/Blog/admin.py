from django.contrib import admin
from . import models

# Register your models here.
class Adminmode(admin.ModelAdmin):
    list_display = ["name","description"]
    search_fields = ["name","description"]



admin.site.register(models.My_Blog,Adminmode)