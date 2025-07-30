from django.urls import path
from .views import register, activate, login_view, confirm_logout, logout_view, my_profile, change_password, forget_password, password_reset_confirm, edit_profile



app_name="accounts"

urlpatterns = [
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("my_profile/", my_profile, name="my_profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("register/", register, name="register"),
    path("change_password/", change_password, name="change_password"),
    path("login/", login_view, name="login"),
    path("confirm_logout/", confirm_logout, name="confirm_logout"),
    path("logout/", logout_view, name="logout"),

    path("password-reset-validation/<uidb64>/<token>/", password_reset_confirm, name="password_reset_confirm"),
    path("password_reset/", forget_password, name="password_reset"),

]