from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmailVerification
from django.core.mail import send_mail

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_active=False  
        )
        
        verification, created = EmailVerification.objects.get_or_create(user=user)
        code = verification.generate_code()
        
        send_mail(
            'Подтверждение регистрации',
            f'Ваш код подтверждения: {code}',
            'rovda.roman@mail.ru',
            [user.email],
            fail_silently=False,
        )
        
        return user
