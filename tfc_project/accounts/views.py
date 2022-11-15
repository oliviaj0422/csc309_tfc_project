from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveAPIView, ListAPIView, \
    CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CardSerializer
from .models import CustomUser, Card


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return Response({})


class CreateCardView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CardSerializer

    def get(self, request, *args, **kwargs):
        return Response({})

    def perform_create(self, serializer):
        serializer.save(holder=self.request.user)
        self.request.user.is_subscribed = True


class EditProfileView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


    def get(self, request, *args, **kwargs):
        return Response({})

    def patch(self, request, *args, **kwargs):
        user_obj = self.get_object()
        data = request.data
        if user_obj == self.request.user:
            user_obj.username = data.get('username', user_obj.username)
            user_obj.set_password = data.get('password', user_obj.password)
            user_obj.email = data.get('email', user_obj.email)
            user_obj.first_name = data.get('first_name', user_obj.first_name)
            user_obj.last_name = data.get('last_name', user_obj.last_name)
            user_obj.avatar = data.get('avatar', user_obj.avatar)
            user_obj.phone_num = data.get('phone_num', user_obj.phone_num)

            user_obj.save()
            serializer = CustomUserSerializer(user_obj)
            return Response(serializer.data)
        return Response({'error': 'Unauthorized.'})


class UpdateCardView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def patch(self, request, *args, **kwargs):
        card_obj = self.get_object()
        data = request.data

        if card_obj.holder == self.request.user:
            card_obj.card_num = data.get('card_num', card_obj.card_num)
            card_obj.billing_addr = data.get('billing_addr', card_obj.billing_addr)
            card_obj.expires_at = data.get('expires_at', card_obj.expires_at)
            card_obj.cvv = data.get('cvv', card_obj.cvv)
            card_obj.pmt_option = data.get('pmt_option', card_obj.pmt_option)
            card_obj.holder = data.get('holder', card_obj.holder)

            card_obj.save()
            serializer = CardSerializer(card_obj)

            return Response(serializer.data)
        return Response({'error': 'You have no permissions to update this card.'})




