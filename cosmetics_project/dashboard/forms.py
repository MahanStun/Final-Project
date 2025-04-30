from django import forms
from .models import *
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("profile_image", "biography_text")


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']  # اضافه کردن فیلد تصویر

    image = forms.ImageField(required=False)  # تصویر اختیاری
from django import forms

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")



# forms.py
from django import forms
from .models import Product_dashboard

class ProductDashboardForm(forms.ModelForm):
    class Meta:
        model = Product_dashboard
        fields = ['Product_name', 'price', 'category', 'picture', 'picture2', 'picture3', 'is_sale', 'sale_price']
        widgets = {
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'Product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }



# forms.py


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category_dashboard
        fields = ['name', 'slug']  # اضافه کردن slug
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'مقدار slug را وارد کنید'}),
        }
