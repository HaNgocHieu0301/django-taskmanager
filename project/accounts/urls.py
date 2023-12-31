from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path("signup", views.SignUp.as_view(), name="signup"),
    path("login", views.CustomLoginView.as_view(), name="login"),
    # path("logout", views.CustomLogoutView.as_view(), name="logout"),
    path("logout", LogoutView.as_view(next_page='login'), name="logout"),
]
