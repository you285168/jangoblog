"""jangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^users/', include('users.urls')),
    #将auth应用中的urls模块包含进来
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'', include('comments.urls')),
]
