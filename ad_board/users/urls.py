from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('activate/', ActivateAccount.as_view(), name='activate_account'),
    # path('signup/', RegisterView.as_view(template_name='account/signup.html'), name='signup'),
    # path('resend_code/', resend_code, name='resend_code'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
]
