from django.urls import path
from . import views


urlpatterns = [
    path("home", views.IndexView.as_view(), name="home"),
    path("", views.IndexView.as_view(), name="home"),
]
