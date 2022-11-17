from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveAPIView, ListAPIView, \
    CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CardSerializer, PaymentSerializer
from .models import CustomUser, Card, Payment
import datetime


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer


class CreateCardView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        serializer.save(holder=self.request.user)
        self.request.user.is_subscribed = True


class EditProfileView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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
            user_obj.pmt_option = data.get('pmt_option',
                                           user_obj.pmt_option)
            if user_obj.pmt_option == 'N':
                user_obj.is_subscribed = False
            elif user_obj.pmt_option == 'M' and\
                Card.objects.filter(holder=user_obj).exists():
                user_obj.is_subscribed = True
                pending_pmt = Payment.objects.filter(pmt_status='PD')
                pending_pmt.amount = 14.99
                pending_pmt.recur = 'Monthly'
            elif user_obj.pmt_option == 'Y' and \
                Card.objects.filter(holder=user_obj).exists():
                user_obj.is_subscribed = True
                pending_pmt = Payment.objects.filter(pmt_status='PD')
                pending_pmt.amount = 149.99
                pending_pmt.recur = 'Yearly'
            user_obj.save()
            serializer = CustomUserSerializer(user_obj)
            return Response(serializer.data)
        return Response({'error': 'Unauthenticated.'})


class UpdateCardView(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def patch(self, request, *args, **kwargs):
        card_obj = self.get_object()
        data = request.data

        if card_obj.holder == self.request.user:
            card_obj.card_num = data.get('card_num', card_obj.card_num)
            card_obj.billing_addr = data.get('billing_addr',
                                             card_obj.billing_addr)
            card_obj.expires_at = data.get('expires_at', card_obj.expires_at)
            card_obj.cvv = data.get('cvv', card_obj.cvv)
            card_obj.holder = data.get('holder', card_obj.holder)

            card_obj.save()
            serializer = CardSerializer(card_obj)

            return Response(serializer.data)
        return Response({'error': 'You have no permissions to update this '
                                  'card.'})


class PaymentHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.filter()
    serializer_class = PaymentSerializer




