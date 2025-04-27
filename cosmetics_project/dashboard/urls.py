from django.urls import path
from .views import *

urlpatterns = [
    path("",DashboardView.as_view(),name="dashboard"),
    path('add_blog/', add_blog, name='add_blog'),
    path('delete_blog/<int:blog_id>/', delete_blog, name='delete_blog'),
]
