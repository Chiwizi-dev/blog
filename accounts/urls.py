from django.urls import path
from .views import register, activate, login_view, confirm_logout, logout_view, dashboard



app_name="accounts"

urlpatterns = [
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("confirm_logout/", confirm_logout, name="confirm_logout"),
    path("logout/", logout_view, name="logout"),

]