# api/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny
from .models import User, OTPHandler
from .serializers import RegisterSerializer

# for JWT creation
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class SendOTPAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({"detail": "mobile is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp_row = OTPHandler.objects.create(
            mobile=mobile,
            otp=1234
        )

        return Response({
            "request_id": str(otp_row.request_id),
            "otp": otp_row.otp,
            "mobile": mobile
        }, status=status.HTTP_201_CREATED)


class VerifyOTPAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        req_id = request.data.get('request_id')
        otp = int(request.data.get('otp'))
        mobile = request.data.get('mobile')
        if not req_id or not otp:
            return Response({"detail": "req_id and otp required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_row = OTPHandler.objects.get(request_id=req_id)
        except OTPHandler.DoesNotExist:
            return Response({"detail": "invalid req_id"}, status=status.HTTP_404_NOT_FOUND)


        if otp_row.attempts >= 5:
            return Response({"detail": "Too many attempts"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if (otp!=otp_row.otp):
            otp_row.attempts += 1
            otp_row.save(update_fields=['attempts'])
            return Response({"detail": "invalid otp"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(mobile=mobile)

        refresh = RefreshToken.for_user(user)
        refresh['id'] = str(user.id)
        refresh['mobile'] = user.mobile
        refresh['role'] = user.role

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "access": access_token,
            "refresh": refresh_token,
            "user": {
                "id": user.id,
                "mobile": user.mobile,
                "role": user.role,
            }
        }, status=status.HTTP_200_OK)
