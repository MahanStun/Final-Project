from django.db import models
from django.contrib.auth.models import User
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

class UserProfile_Default(models.Model):
    profile_image = models.ImageField(upload_to="uploads/user",blank=True,null=True)
    
    def __str__(self):
        return "Deafult Image"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='uploads/user', default='uploads/user/default_profile.png', blank=True)

    biography_text = models.TextField(blank=True)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username
    
class Ticket(models.Model):
    STATUS_CHOICES = (
        ("open","open"),
        ("closed","closed"),
        ("banned","banned")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} => {self.subject} "
    



class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="upload/cosmetics_picture/")
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return self.title





class Category_dashboard(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(default=None,blank=True,null=True)

    def __str__(self):
        return self.name

class Product_dashboard(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    category = models.ForeignKey(Category_dashboard, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="upload/cosmetics_picture/", blank=True, null=True)
    picture2 = models.ImageField(upload_to="upload/cosmetics_picture/", blank=True, null=True)
    picture3 = models.ImageField(upload_to="upload/cosmetics_picture/", blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    likes = models.ManyToManyField(User, related_name="liked_products", blank=True)  # اضافه کردن فیلد لایک

    def total_likes(self):
        return self.likes.count()  # تعداد کل لایک‌ها

    def __str__(self):
        return self.name


class Comment_dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_dashboard, on_delete=models.CASCADE, null=False)  # مقدار NULL مجاز نیست
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"