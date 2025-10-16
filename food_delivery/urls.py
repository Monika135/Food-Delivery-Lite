"""
URL configuration for food_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import render


def index(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')


def partner_dashboard(request):
    return render(request, 'partner_dashboard.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def chat_view(request, booking_id):
    return render(request, 'chat.html', {"booking_id": str(booking_id)})


urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('customer/dashboard/', customer_dashboard, name='customer'),
    path('partner/dashboard/', partner_dashboard, name='partner'),
    path('admin/dashboard/', admin_dashboard, name='admin'),
    # path('chat/<uuid:booking_id>/', chat_view, name='chat'),
    path('users/', include('users.urls')),
    path('bookings/', include('bookings.urls'))
]
