from django import forms
from .models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("profile_image","biography_text") 


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']  # اضافه کردن فیلد تصویر

    image = forms.ImageField(required=False)  # تصویر اختیاری
