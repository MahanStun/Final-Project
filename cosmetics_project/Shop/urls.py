from django.urls import path
from .views import UserEditView
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.index_shop, name="index_shop"),
    path("login/", views.login_user, name="login_url"),
    path("signup/", views.signup_user, name="signup_url"),
    path("logout/", views.logout_user, name="logout_url"),
    # path("password/", auth_views.PasswordChangeView.as_view(template_name='Shop/change_password.html')),
    path("setting/", UserEditView.as_view() ,name="setting"),
    path("quiz_result/", views.quiz_view ,name="quiz_result"),
    path("verifycation_code/", views.verifycation_code ,name="verifycation_code"),
    path("verify_code/", views.verify_code ,name="verify_code"),
    path("resend_code/", views.resend_code ,name="resend_code"),
    path("exam/", views.exam ,name="exam"),
]