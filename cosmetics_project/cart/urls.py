from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path("",views.cart_summary,name="cart_summary"),
    path("add/",views.cart_add,name="cart_add"),
    path("delete/",views.cart_delete,name="cart_remove"),
    path("update/",views.cart_update,name="update"),
    path("pay/",payment_zarinpal, name="zarinpal"),
    path("verify/", verify_payment, name="verify_payment"),
    path("finding_product/",find_product, name="finding"),
]

