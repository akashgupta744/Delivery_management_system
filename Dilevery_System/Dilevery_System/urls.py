"""
URL configuration for Dilevery_System project.

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
from django.conf import settings
from django.conf.urls.static import static
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('adminlogin/',adminlogin,name='adminlogin'),
    path('pic/<int:id><int:n>',pic,name='pic'),
    path('employeelogin/',employeelogin,name='employeelogin'),
    path('employeesignup/',employeesignup,name='employeesignup'),
    path('customerlogin/',customerlogin,name='customerlogin'),
    path('customersignup/',customersignup,name='customersignup'),
    path('track/',track,name='track'),
    path('forget/',forget,name='forget'),
    path('otp/',otp_p,name='otp'),
    path('change_password/',change_password,name='change_password'),
    path('employeelist/',employeelist,name='employeelist'),
    path('customerlist/',customerlist,name='customerlist'),
    path('order_create/',order_create,name='order_create'),
    path('delivery_status/',delivery_status,name='delivery_status'),
    path('camera/<int:id><int:n>',camera,name='camera'),
    path('success/<int:id>',success,name='success'),
    path('logout/',logoutall,name='logout'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
