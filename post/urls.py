from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('catagories/', views.CategoryView.as_view(), name='categories'),
    path('detail/<int:post_id>/', views.PostDetailView.as_view(), name='detail'),

]