from accounts.models import Payment, CustomUser, Card
from django.core.management.base import BaseCommand, CommandError
import datetime
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Pay for the most recently dued pending payment.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str,
                            help='Please indicate your username.')

    def handle(self, *args, **options):
        name = options['username']
        try:
            user = CustomUser.objects.get(username=name)
        except CustomUser.DoesNotExist:
            raise CommandError('User "%s" does not exist' % name)

        card_objs = Card.objects.filter(holder=user)
        payments = Payment.objects.none()
        if card_objs:
            for card_obj in card_objs:
                payments = payments | Payment.objects.filter(
                    pmt_method=card_obj.card_num, pmt_status='PD')
        else:
            self.stdout.write("Please register a card first .")
        if payments:
            pmt_to_pay = payments.order_by('pmt_date')[0]
            if datetime.date.today() == pmt_to_pay.pmt_date.date():
                if pmt_to_pay.pmt_method is not None:
                    pmt_to_pay.pmt_status = 'PA'
                    if payments.count() > 1: # more payments to pay
                        user.sub_edate = payments.order_by('pmt_date')[1]

                    else: # paid all payments within the end date
                        next_edate = pmt_to_pay.pmt_date \
                                                  + relativedelta(years=1)
                        if user.pmt_option == 'M':
                            next_edate = pmt_to_pay.pmt_date \
                                         + relativedelta(months=1)
                        pmt_edate = pmt_to_pay.edate
                        user.sub_edate = min(pmt_edate, next_edate)
                    pmt_to_pay.save()
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        'Payment successfully made.'))
                else:
                    self.stdout.write("Please register a card first .")
            elif datetime.date.today() > pmt_to_pay.pmt_date.date():
                user.is_subscribed = False
                user.pmt_option = 'N'
                user.save()
                self.stdout.write("You have overdue payments. "
                                  "Please reactivate your subscription.")
            else:
                self.stdout.write(f'No payments are due at the moment. Your '
                                  f'next payment is due '
                                  f'{pmt_to_pay.pmt_date.date()}')
        else:
            self.stdout.write("No pending payments to be made in your account.")


