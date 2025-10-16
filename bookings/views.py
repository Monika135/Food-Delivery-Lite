from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from .models import Booking, Product, BookingStatus
from users.models import User


class BookingHandler(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		user = request.user

		if user.role not in ['customer', 'admin']:
			return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

		try:
			product = Product.objects.get(id=request.data.get('product_id'))
		except Product.DoesNotExist:
			return Response({"message": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

		quantity = int(request.data.get('quantity', 1))
		if quantity <= 0:
			return Response({"message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

		if product.quantity < quantity:
			return Response({"message": "Out of stock"}, status=status.HTTP_400_BAD_REQUEST)

		product.quantity -= quantity
		product.save(update_fields=['quantity'])

		total_price = product.price * quantity

		booking = Booking.objects.create(
			customer=user,
			product=product,
			ordered_quantity=quantity,
			created_by=user
		)

		return Response({
			"message": "Booking created successfully",
			"total_price": total_price,
			"ordered_quantity": quantity,
			"booking_id": str(booking.id),
			"customer_id": str(user.id),
			"product_id": str(product.id),
		}, status=status.HTTP_201_CREATED)

	def get(self, request):
		user = request.user

		if user.role not in ['customer', 'admin']:
			return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

		booking_id = request.data.get("booking_id")

		if booking_id:
			try:
				booking = Booking.objects.get(id=booking_id)
			except Booking.DoesNotExist:
				return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

			# Only admin or the customer who made it can view
			if user.role != 'admin' and booking.customer != user:
				return Response({"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

			return Response({
				"booking_id": str(booking.id),
				"customer": booking.customer.name,
				"product": booking.product.name,
				"quantity": booking.ordered_quantity,
				"price": booking.product.price,
				"status": booking.status.status if booking.status else "Pending",
				"created_at": booking.created_at,
				"is_active": booking.is_active,
				"created_by": booking.created_by.name if booking.created_by else None,
				"canceled_by": booking.canceled_by.name if booking.canceled_by else None
			}, status=status.HTTP_200_OK)

		if user.role == 'admin':
			bookings = Booking.objects.all().order_by('-created_at')
		else:
			bookings = Booking.objects.filter(customer=user).order_by('-created_at')

		data = [{
			"booking_id": str(b.id),
			"customer": b.customer.name,
			"product": b.product.name,
			"quantity": b.ordered_quantity,
			"price": b.product.price,
			"status": b.status.status if b.status else "Pending",
			"created_at": b.created_at,
			"is_active": b.is_active,
			"created_by": b.created_by.name if b.created_by else None,
			"canceled_by": b.canceled_by.name if b.canceled_by else None,
			"partner_id": str(b.partner.id) if b.partner else '',
			"partner_name": b.partner.name if b.partner else ''

		} for b in bookings]

		return Response(data, status=status.HTTP_200_OK)

	def patch(self, request):
		user = request.user

		if user.role not in ['customer', 'admin']:
			return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

		booking_id = request.data.get('booking_id')
		try:
			booking = Booking.objects.get(id=booking_id)
		except Booking.DoesNotExist:
			return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

		# Only admin or the customer who created it can cancel
		if user.role != 'admin' and booking.customer != user:
			return Response({"message": "You can only cancel your own bookings"}, status=status.HTTP_403_FORBIDDEN)

		if not booking.is_active:
			return Response({"message": "Booking already canceled"}, status=status.HTTP_400_BAD_REQUEST)

		booking.is_active = False
		booking.updated_at = timezone.now()
		booking.canceled_by = user
		booking.save(update_fields=['is_active', 'updated_at', 'canceled_by'])

		return Response({
			"message": "Booking cancelled successfully",
			"booking_id": str(booking.id),
			"canceled_by": user.name
		}, status=status.HTTP_200_OK)



class AssignBookingHandler(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		user = request.user

		if user.role != 'admin':
			return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

		booking_id = request.data.get('booking_id')
		partner_id = request.data.get('partner_id')

		try:
			booking = Booking.objects.get(id=booking_id)
		except Booking.DoesNotExist:
			return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

		try:
			partner = User.objects.get(id=partner_id, role='partner')
		except User.DoesNotExist:
			return Response({"message": "Partner not found"}, status=status.HTTP_404_NOT_FOUND)


		booking.partner = partner
		booking.save(update_fields=['partner'])

		return Response({
			"message": "Booking assigned successfully",
			"booking_id": str(booking.id),
			"partner_id": str(partner.id),
			"partner_name": partner.name
		}, status=status.HTTP_200_OK)


class BookingStatusHandler(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def patch(self, request):
		user = request.user

		if user.role != 'partner':
			return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

		booking_id = request.data.get('booking_id')
		new_status = request.data.get('status')

		valid_statuses = ["Start", "Reached", "Collected", "Delivered"]
		if new_status not in valid_statuses:
			return Response({"message": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			booking = Booking.objects.get(id=booking_id, partner=user)
		except Booking.DoesNotExist:
			return Response({"message": "Booking not found or not assigned to you"}, status=status.HTTP_404_NOT_FOUND)

		status_obj, _ = BookingStatus.objects.get_or_create(status=new_status)
		booking.status = status_obj
		booking.updated_at = timezone.now()
		booking.save(update_fields=['status', 'updated_at'])

		return Response({
			"message": "Status updated successfully",
			"booking_id": str(booking.id),
			"new_status": new_status
		}, status=status.HTTP_200_OK)
	

	def get(self, request):
		user = request.user

		if user.role != 'partner':
			return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

		bookings = Booking.objects.filter(partner=user)
		bookings = bookings.order_by('-created_at')

		data = [{
			"booking_id": str(b.id),
			"customer": b.customer.name,
			"product": b.product.name,
			"status": b.status.status if b.status else None,
			"is_active": b.is_active,
			"created_at": b.created_at,
			"updated_at": b.updated_at
		} for b in bookings]

		return Response(data, status=status.HTTP_200_OK)





