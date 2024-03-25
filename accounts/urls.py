from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('register/otp/', views.UserSendOtpCode.as_view(), name='user-otp-verify'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', views.UserEditProfileView.as_view(), name='edit-profile'),
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
]