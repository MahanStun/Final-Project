from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from Blog.views import PasswordssChangeView

urlpatterns = [
    path("", views.index ,name='index_blog'),
    path("all-posts/<str:slug>", views.single_post),
    path("password/", PasswordssChangeView.as_view(template_name='Shop/change_password.html'), name="password"),
    path("password_success", views.password_success, name="password_success"),
]