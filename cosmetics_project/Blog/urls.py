from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import GetAllData , PostData , PostModelData

urlpatterns = [
    path("get-all-data/", GetAllData.as_view()),
    path("post-model/", PostModelData.as_view()),
    path("post-data/", PostData.as_view()),
    path("", views.blog_list, name="index_blog"),
]