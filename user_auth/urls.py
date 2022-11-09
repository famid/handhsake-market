from django.urls import path
from . import views
from handshake_market.views import home

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.custom_logout, name="logout"),
]
