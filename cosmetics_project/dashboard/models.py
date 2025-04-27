from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile_Default(models.Model):
    profile_image = models.ImageField(upload_to="uploads/user",blank=True,null=True)
    
    def __str__(self):
        return "Deafult Image"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="uploads/user",blank=True,null=True)
    biography_text = models.TextField(max_length=800,blank=True,null=True)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
