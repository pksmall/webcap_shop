"""
webcap_shop URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # web admin
    path('admin/', admin.site.urls),

    # api endpoints
    path('user/auth/', include('users.urls')),
    path('store/', include('store.urls'))
]
