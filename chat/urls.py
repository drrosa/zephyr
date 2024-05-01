from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/signup/", views.signup, name="signup"),
    path("<int:pk>/edit/", views.MessageEdit.as_view(), name="message_edit"),
    path("<int:pk>/delete/", views.MessageDelete.as_view(), name="message_delete"),
]
