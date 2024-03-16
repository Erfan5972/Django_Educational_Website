from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.UserRegisterView.as_view(), name='user-register'),
]