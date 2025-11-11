from django.contrib.auth.models import AbstractUser
from django.db import models
import re


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.phone_number or self.email

    def clean(self):
        super().clean()
        if self.phone_number:
            # Remove any non-digit characters except +
            phone = re.sub(r'[^\d+]', '', self.phone_number)
            if not phone.startswith('+'):
                # Assume Indian number if no country code
                if len(phone) == 10:
                    phone = '+91' + phone
            self.phone_number = phone


class PasswordResetOTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number', 'otp']),
        ]

    def __str__(self):
        return f"OTP for {self.phone_number}"

