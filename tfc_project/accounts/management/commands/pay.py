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
        if payments:
            pmt_to_pay = payments.order_by('pmt_date')[0]
            if datetime.date.today() == pmt_to_pay.pmt_date.date():
                if pmt_to_pay.pmt_method is not None:
                    pmt_to_pay.pmt_status = 'PA'
                    # if len(payments) > 1: # more payments to pay
                    #     user.sub_edate = payments.order_by('pmt_date')[1]
                    # else: # paid all payments within the end date
                    #     if user.pmt_option == 'Y':
                    #         user.sub_edate = pmt_to_pay.pmt_date \
                    #                          + relativedelta(years=1)
                    #     else:
                    #         user.sub_edate = pmt_to_pay.pmt_date \
                    #                          + relativedelta(months=1)
                    #         user.pmt_option = 'N'
                    pmt_to_pay.save()
                    self.stdout.write(self.style.SUCCESS(
                        'Payment successfully made.'))
                else:
                    self.stdout.write("Please register a card first .")
            else:
                self.stdout.write(f'No payments are due at the moment. Your '
                                  f'next payment is due '
                                  f'{pmt_to_pay.pmt_date.date()}')
        else:
            self.stdout.write("No pending payments to be made in your account.")


