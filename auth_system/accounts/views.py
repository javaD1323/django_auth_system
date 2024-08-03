from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OTPRequestSerializer, OTPVerifySerializer, LoginSerializer, UserSerializer
from .utils import get_client_ip, record_failed_attempt, send_otp, verify_otp, authenticate_user
from .decorators import check_ip_block
from .models import User


class RequestOTPView(APIView):
    @check_ip_block
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                return Response({'detail': 'User already registered. try to login'}, status=status.HTTP_400_BAD_REQUEST)
            code = send_otp(phone_number)
            return Response({'detail': f'OTP sent successfully. code : {code}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    @check_ip_block
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            full_name = request.data.get('full_name')
            email = request.data.get('email')
            password = request.data.get('password')

            if not full_name or not email or not password:
                return Response({'error': 'Full name, email, and password are required.'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                verify_otp(phone_number, code)
                user = User.objects.create_user(phone_number, full_name, email, password)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                record_failed_attempt(get_client_ip(request))
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) # raise insted of error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @check_ip_block
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate_user(phone_number, password)
            if user:
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            record_failed_attempt(get_client_ip(request))
            return Response({'error': 'Invalid phone number or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
