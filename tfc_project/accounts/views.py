from dateutil.relativedelta import relativedelta
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CardSerializer, \
    MembershipPlanSerializer, PaymentSerializer
from .models import CustomUser, Card, Payment, MembershipPlan
import datetime
from classes.models import UserEnrolledClass


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
        """Updates user profile. If users canceled subscription,
        cancel all future payments."""
        user_obj = self.get_object()
        data = request.data
        if user_obj == self.request.user:
            # update all fields
            user_obj.username = data.get('username', user_obj.username)
            user_obj.set_password = data.get('password', user_obj.password)
            user_obj.email = data.get('email', user_obj.email)
            user_obj.first_name = data.get('first_name', user_obj.first_name)
            user_obj.last_name = data.get('last_name', user_obj.last_name)
            user_obj.avatar = data.get('avatar', user_obj.avatar)
            user_obj.phone_num = data.get('phone_num', user_obj.phone_num)
            old_pmt_option = user_obj.pmt_option
            user_obj.pmt_option = data.get('pmt_option',
                                           user_obj.pmt_option)
            # if an user cancels subscription, change subscription status, also
            # drop from any enrolled classes.
            if user_obj.pmt_option == 'N':
                user_obj.is_subscribed = False
                enrolled_classes = UserEnrolledClass.objects.filter(
                    user_id=user_obj.id)
                if enrolled_classes:
                    enrolled_classes.delete()
            # check if an user has pending payments or cancelled payments.
            # If so, update them or create new ones to
            # reflect the new plan option.
            if Card.objects.filter(holder=user_obj).exists():
                card_objs = Card.objects.filter(holder=user_obj)
                if card_objs:
                    for card_obj in card_objs:
                        pending_payments = \
                            Payment.objects.filter(pmt_method=card_obj.card_num,
                                                   pmt_status='PD').order_by(
                                'pmt_date')
                        canceled_pmts = \
                            Payment.objects.filter(pmt_method=card_obj.card_num,
                                                               pmt_status='C')
                        if pending_payments or canceled_pmts:
                            paid_payment = Payment.objects.filter(pmt_method=
                                                card_obj.card_num, pmt_status=
                            'PA').order_by('-pmt_date')[0]
                            # if cancel plan, cancel all future payments
                            if user_obj.pmt_option == 'N':
                                if pending_payments:
                                    pending_payments.update(pmt_status='C')
                            # if change to monthly plan, update existing pending
                            # payments
                            elif user_obj.pmt_option == 'M':
                                # if no pending payments, create new ones.
                                user_obj.is_subscribed = True
                                new_pmt = Payment(
                                    amount=MembershipPlan.objects.get(type=
                                                                    'M').price,
                                    pmt_date=paid_payment.pmt_date + \
                                             relativedelta(months=1),
                                    recur = 'Monthly',
                                    edate = datetime.date.today() + \
                                            relativedelta(years=1),
                                    pmt_method = card_obj.card_num,
                                    payer=user_obj.username,
                                )
                                # else, update price and payment date to match
                                # the new plan
                                if pending_payments:
                                    print(pending_payments)
                                    first_unpaid_pmt = pending_payments[0]
                                    new_pmt.pmt_date = first_unpaid_pmt.pmt_date
                                    new_pmt.edate = first_unpaid_pmt.edate
                                    if old_pmt_option == 'Y':
                                        pending_payments.delete()
                                new_pmt.save()
                            # if change to yearly plan, update payments
                            elif user_obj.pmt_option == 'Y':
                                user_obj.is_subscribed = True
                                new_pmt = Payment(
                                    amount=MembershipPlan.objects.get(type=
                                                                    'Y').price,
                                    pmt_date=paid_payment.pmt_date
                                             + relativedelta(years=1),
                                    recur = 'Yearly',
                                    edate = datetime.date.today()
                                            + relativedelta(years=1),
                                    pmt_method = card_obj.card_num,
                                    payer=user_obj.username
                                )
                                if pending_payments:
                                    first_unpaid_pmt = pending_payments[0]
                                    new_pmt.pmt_date = first_unpaid_pmt.pmt_date
                                    new_pmt.edate = first_unpaid_pmt.edate
                                    print(f'{new_pmt.edate}')
                                    if old_pmt_option == 'M':
                                        pending_payments.delete()
                                new_pmt.save()

            user_obj.save()
            serializer = CustomUserSerializer(user_obj)
            return Response(serializer.data)
        return Response({'error': 'Unauthenticated.'})


class UpdateCardView(UpdateAPIView):
    """Only updates billing address and expiry date. Otherwise, users need to
    register a new card.
    """

    permission_classes = [IsAuthenticated]
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def patch(self, request, *args, **kwargs):
        card_obj = self.get_object()
        data = request.data

        if card_obj.holder == self.request.user:
            card_obj.billing_addr = data.get('billing_addr',
                                             card_obj.billing_addr)
            card_obj.expires_at = data.get('expires_at', card_obj.expires_at)

            card_obj.save()
            print(card_obj)

            serializer = CardSerializer(card_obj)

            return Response(serializer.data)
        return Response({'error': 'You have no permissions to update this '
                                  'card.'})


class ListPagination(PageNumberPagination):
    page_size=5


class PaymentHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    pagination_class = ListPagination

    def get_queryset(self):
        payments = Payment.objects.filter(payer=self.request.user.username)
        return payments.order_by('pmt_date')


class MembershipView(ListAPIView):
    serializer_class = MembershipPlanSerializer
    pagination_class = ListPagination


