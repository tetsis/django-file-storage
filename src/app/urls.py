"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # GCP
    path('upload/', views.upload, name='upload'),
    path('upload_api/', views.upload_api, name='upload_api'),

    # AWS S3
    path('aws/', views.aws_index, name='aws_index'),
    path('aws_upload/', views.aws_upload, name='aws_upload'),
    path('aws_upload_api/', views.aws_upload_api, name='aws_upload_api'),
    path('media/<str:file>', views.aws_media, name='aws_media'),
]
