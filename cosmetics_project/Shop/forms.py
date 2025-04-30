from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth import validators

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "اسم خود را وارد کنید"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی خود را وارد کنید",
            }
        ),
    )
    email = forms.EmailField(
        label="",
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "ایمیل خود را وارد کنید",
            }
        ),
    )
    username = forms.CharField(
        label="",
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "name": "username",
                "class": "form-control",
                "placeholder": "نام کاربری خود را وارد کنید",
            }
        ),
    )
    password1 = forms.CharField(
        label="",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password1",
                "placeholder": "رمز خود را وارد کنید",
            }
        ),
    )
    password2 = forms.CharField(
        label="",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password2",
                "placeholder": "رمز خود را دوباره وارد کنید",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]



class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="",
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password"}
        ),
    )
    new_password1 = forms.CharField(
        label="",
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
    )
    new_password2 = forms.CharField(
        label="",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
