"""board_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import os
import sys

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import  views

# from board_site.accounts.views  import signup

urlpatterns = [
    # path('', views.redirect_to_home),
    path('',RedirectView.as_view(url='/board')),
    path('board/', include('board.urls')),
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('ueditor/',include('ueditor.urls'),name='ueditor')
]

