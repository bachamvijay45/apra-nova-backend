from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.get_user_profile, name="user-profile"),
    path("callback/", views.oauth_callback, name="oauth-callback"),
    path("update-role/", views.update_user_role, name="update-role"),
]
