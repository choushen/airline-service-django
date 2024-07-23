"""airline_service_project URL Configuration

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

from rest_framework.urlpatterns import format_suffix_patterns
from airlines import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/findflight/', views.FindFlight.as_view()),
    path('api/bookflight/', views.BookFlight.as_view()),
    path('api/paymentmethods/', views.PaymentMethods.as_view()),
    path('api/payforbooking/', views.PayForBooking.as_view()),
    path('api/finalizebooking/', views.FinalizeBooking.as_view()),
    path('api/bookingstatus/', views.BookingStatus.as_view()),
    path('api/cancelbooking/', views.CancelBooking.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


