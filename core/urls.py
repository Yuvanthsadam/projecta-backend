"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_countries import settings
from core import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.customTokenClaims import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/token/', MyTokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
    # my app urls
    path('api/', include('accounts.api.urls')),
    path('invest/',include('invest.urls')),
    path('resume/', include('resume.api.urls')),
    path('social/', include('social.api.urls')),
    path('api/support/',include('support.api.urls')),
]
if settings.DEBUG:  # Dev only
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
# static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)