from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UserEditView
urlpatterns = [
    path("", views.index_shop, name="index_shop"),
    path("Products_Cosmetics/<int:pk>", views.Products_Cosmetics, name="Products_Cosmetics"),
    path("login/", views.login_user, name="login_url"),
    path("signup/", views.signup_user, name="signup_url"),
    path("logout/", views.logout_user, name="logout_url"),
    path("password/", views.PasswordssChangeView.as_view(template_name='shop/change_password.html'), name="password"),
    path('Password_email_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path("password_success", views.password_success, name="password_success"),
    path("verifycation_code/", views.verifycation_code ,name="verifycation_code"),
    path("verify_code/", views.verify_code ,name="verify_code"),
    path("resend_code/", views.resend_code ,name="resend_code"),
    path("verify_reset_code/", views.verify_reset_code ,name="verify_reset"),
    path("forgot_password/", views.forgot_password ,name="forgot_password"),
    path("category/<str:cat>", views.category, name="category_url"),
    path("error_category", views.category, name="errorPage"),
    path("get_comments/", views.get_comments, name="get_comments"),
    path("add_comment/", views.add_comment, name="add_comment"),
    path('delete-comment/', views.delete_comment, name='delete_comment'),
    path("setting/", UserEditView.as_view() ,name="setting"),
    path('check_comments/', views.check_comments, name='check_comments'),

]