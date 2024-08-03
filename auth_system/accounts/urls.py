
from django.urls import path
from .views import RequestOTPView, VerifyOTPView, LoginView

urlpatterns = [
    path('api/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/login/', LoginView.as_view(), name='login'),
]
