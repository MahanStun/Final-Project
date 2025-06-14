from django.urls import path
from .views import *

urlpatterns = [
    path("",DashboardView.as_view(),name="dashboard"),
    path('add_blog/', add_blog, name='add_blog'),
    path('delete_blog/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('dashboard/add-product/', add_product_dash, name='add_product_dash'),
    path('dashboard/delete-product/<int:product_id>/', delete_product_dash, name='delete_product_dash'),
    path('add-category/', add_category, name='add_category'),
    path('edit-blog/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),

]



