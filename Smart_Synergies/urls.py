from django.contrib import admin
from django.urls import path
from Ai_Django.views import (
    signup,
    forgot,
    SignupAPIView,
    ForgotPasswordAPIView,
)
urlpatterns = [
]

accounts_api_urls = [
          path('api/accounts/signup/',SignupAPIView(),name='signup_api'),
          path('api/accounts/forgot-password-request/',ForgotPasswordAPIView(),name='forgot_password'),

]
template_urls = [
    path("signup/",view=signup,name='signup'),
    path("forgot/",view=forgot,name='forgot')

]