from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
import re
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name', 'phone_number')

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required")
        # Normalize phone number
        phone = re.sub(r'[^\d+]', '', value)
        if not phone.startswith('+'):
            if len(phone) == 10:
                phone = '+91' + phone
            else:
                raise serializers.ValidationError("Invalid phone number format")
        return phone

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 
                  'address', 'city', 'state', 'zip_code', 'is_email_verified', 'is_phone_verified', 'created_at')
        read_only_fields = ('id', 'is_email_verified', 'is_phone_verified', 'created_at')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone_number',
                  'address', 'city', 'state', 'zip_code')
        read_only_fields = ('id', 'email', 'username', 'phone_number')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required")
        # Normalize phone number
        phone = re.sub(r'[^\d+]', '', value)
        if not phone.startswith('+'):
            if len(phone) == 10:
                phone = '+91' + phone
            else:
                raise serializers.ValidationError("Invalid phone number format")
        return phone


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    otp = serializers.CharField(required=True, max_length=6)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required")
        # Normalize phone number
        phone = re.sub(r'[^\d+]', '', value)
        if not phone.startswith('+'):
            if len(phone) == 10:
                phone = '+91' + phone
            else:
                raise serializers.ValidationError("Invalid phone number format")
        return phone

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

