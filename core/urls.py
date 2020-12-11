"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings

from rest_framework import routers
from api.views import PostViewSet, TaggedPostViewSet

router = routers.DefaultRouter()
router.register(r'tag', TaggedPostViewSet)
router.register(r'post', PostViewSet)
router.register(r'', PostViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

if settings.ENV == 'DEV':
    urlpatterns.append(path('admin/', admin.site.urls))
