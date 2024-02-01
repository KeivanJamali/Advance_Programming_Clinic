"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from clinic.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register_or_login/", register_or_login, name="register_or_login"),
    path("secretary_register/", secretary_register, name="secretary_register"),
    path("secretary_page/", secretary_page, name="secretary_page"),
    path("doctor_page/", doctor_page, name="doctor_page"),
    path("customer/", customer_page, name="customer_page"),
    path("select_patient/", select_patient, name="select_patient")
]
