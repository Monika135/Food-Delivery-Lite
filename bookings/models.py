from django.db import models
from django.conf import settings
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BookingStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status=models.CharField(max_length=20,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_bookings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='partner_bookings', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(BookingStatus, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    ordered_quantity = models.IntegerField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings_created', on_delete=models.SET_NULL, null=True, blank=True)
    canceled_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings_canceled', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ChatMessage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']