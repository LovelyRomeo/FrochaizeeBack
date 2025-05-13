from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from .models import EmailVerification

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь зарегистрирован."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not all([email, code]):
            return Response({'error': 'Email и код обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.get(user=user)
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            return Response({'error': 'Пользователь или код не найдены.'}, status=status.HTTP_404_NOT_FOUND)

        if verification.code != code:
            return Response({'error': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        verification.code = ''
        verification.save()

        return Response({'detail': 'Email подтвержден. Теперь вы можете войти.'})


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь зарегистрирован."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not all([email, code]):
            return Response({'error': 'Email и код обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.get(user=user)
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            return Response({'error': 'Пользователь или код не найдены.'}, status=status.HTTP_404_NOT_FOUND)

        if verification.code != code:
            return Response({'error': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        verification.code = ''
        verification.save()

        return Response({'detail': 'Email подтвержден. Теперь вы можете войти.'})
