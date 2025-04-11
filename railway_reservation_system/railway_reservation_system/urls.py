"""
URL configuration for railway_reservation_system project.

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
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'trains', views.TrainViewSet)
router.register(r'stations', views.StationViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'passengers', views.PassengerViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'availabilities', views.AvailabilityViewSet)
router.register(r'search', views.SearchViewSet, basename='search')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
]
