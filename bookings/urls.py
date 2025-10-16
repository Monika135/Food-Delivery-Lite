from django.views.generic import RedirectView
from django.urls import path, include
from .views import BookingHandler, AssignBookingHandler, BookingStatusHandler

urlpatterns = [
    path('bookings/', BookingHandler.as_view(), name='booking'),
    path('assign_booking/', AssignBookingHandler.as_view(), name='booking_assigned'),
    path('booking_status/', BookingStatusHandler.as_view(), name='booking_status'),
]