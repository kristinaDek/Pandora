"""pandora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from .views import login_user, homepage, register, logout_user, user_profile
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path
from .views import RegisterAPI
from django.urls import path

urlpatterns = [

    path('login/', login_user, name='login'),
    path('', RedirectView.as_view(url='homepage/')),
    path('homepage/', homepage, name='homepage'),
    path('register/', register, name='register'),
    # path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path('api/register/', RegisterAPI.as_view(), name='register'),
]

