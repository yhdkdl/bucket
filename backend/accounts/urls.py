from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import login_user, register_user, me

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", me, name="me"),
]
