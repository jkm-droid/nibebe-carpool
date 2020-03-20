"""carpool URL Configuration

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
from django.urls import path
from .views import (
    register_user_view,
    login_user_view,
    activate_account_view,
    logout_user_view,
)

urlpatterns = [

    path('register', register_user_view, name='register'),
    path('login', login_user_view, name='login'),
    path('logout', logout_user_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate_account_view, name='activate'),
]
