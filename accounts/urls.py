from django.urls import path
from accounts.views import login_page, signup_page, logout_page, profile, userUpdate, deleteAccount

app_name = 'accounts'

urlpatterns = [
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path("logout/", logout_page, name="logout"),
    path("profile/", profile, name="profile"),
    path("update/", userUpdate, name="update_profile"),
    path("delete/", deleteAccount, name="delete_account"),
]
