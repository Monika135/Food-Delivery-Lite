from django.urls import path
from .views import RegisterAPI, SendOTPAPI, VerifyOTPAPI
urlpatterns = [
    path('create_user/', RegisterAPI.as_view(), name='register'),
    path('send_otp/', SendOTPAPI.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOTPAPI.as_view(), name='verify_otp'),
]

