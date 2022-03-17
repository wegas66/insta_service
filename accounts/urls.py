from django.urls import path
from accounts.views import login_user, signup_user, logout_user, verify, auth_page, profile, userUpdate

app_name = 'accounts'

urlpatterns = [
    path('auth', auth_page, name='auth'),
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('verify/<str:email>/<str:token>', verify, name='verify'),
    path("profile/", profile, name="profile"),
    path("update/", userUpdate, name="update_profile"),
]
