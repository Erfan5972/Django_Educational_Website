from django.contrib import admin
from django.urls import path, include
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('post/', include('post.urls', namespace='post')),
    path('bankgateways/', az_bank_gateways_urls()),

]

