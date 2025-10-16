from django.contrib import admin


from .models import Product, BookingStatus, Booking

admin.site.register(Product)
admin.site.register(BookingStatus)
admin.site.register(Booking)