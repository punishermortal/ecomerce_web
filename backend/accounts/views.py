from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
import re
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
)
from .models import User, PasswordResetOTP


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    
    if phone_number and password:
        # Normalize phone number
        phone_number = re.sub(r'[^\d+]', '', phone_number)
        if not phone_number.startswith('+'):
            if len(phone_number) == 10:
                phone_number = '+91' + phone_number
        
        # Authenticate using phone_number as username (since USERNAME_FIELD is phone_number)
        user = authenticate(username=phone_number, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        # Normalize phone number
        phone_number = re.sub(r'[^\d+]', '', phone_number)
        if not phone_number.startswith('+'):
            if len(phone_number) == 10:
                phone_number = '+91' + phone_number
        
        try:
            user = User.objects.get(phone_number=phone_number)
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Delete old OTPs for this phone number
            PasswordResetOTP.objects.filter(phone_number=phone_number, is_used=False).delete()
            
            # Create new OTP
            otp_obj = PasswordResetOTP.objects.create(
                phone_number=phone_number,
                otp=otp,
                expires_at=timezone.now() + timedelta(minutes=10)
            )
            
            # In production, send OTP via SMS or Email
            # For now, we'll return it in response (remove in production)
            print(f"OTP for {phone_number}: {otp}")  # Remove in production
            
            # Send OTP via email if user has email
            if user.email:
                from django.core.mail import send_mail
                try:
                    send_mail(
                        'Password Reset OTP - NextBloom',
                        f'Your OTP for password reset is: {otp}. This OTP is valid for 10 minutes.',
                        'noreply@nextbloom.com',
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error sending email: {str(e)}")
            
            return Response({
                'message': 'OTP sent to your registered email',
                'otp': otp  # Remove this in production
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Phone number not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        
        # Normalize phone number
        phone_number = re.sub(r'[^\d+]', '', phone_number)
        if not phone_number.startswith('+'):
            if len(phone_number) == 10:
                phone_number = '+91' + phone_number
        
        try:
            # Verify OTP
            otp_obj = PasswordResetOTP.objects.get(
                phone_number=phone_number,
                otp=otp,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            
            # Get user and reset password
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
            
            # Mark OTP as used
            otp_obj.is_used = True
            otp_obj.save()
            
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except PasswordResetOTP.DoesNotExist:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

