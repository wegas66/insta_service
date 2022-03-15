from django.urls import path
from accounts.views import login_user, signup_user, logout_user, verify, auth_page

app_name = 'accounts'

urlpatterns = [
    path('auth', auth_page, name='auth'),
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('verify/<str:email>/<str:token>', verify, name='verify'),
]
