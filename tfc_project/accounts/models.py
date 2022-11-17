import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db.models.signals import post_save

PLAN_OPTS = [
    ('M', 'Monthly Plan $14.99 per month'),
    ('Y', 'Yearly Plan $149.99 per year'),
    ('N', 'Inactive / Cancel plan')
]


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone_num = models.CharField(max_length=10, verbose_name='Phone',
                                 blank=True)
    avatar = models.ImageField(blank=True, null=True)
    is_subscribed = models.BooleanField(default=False,
                                        verbose_name='Subscription status')
    pmt_option = models.CharField(max_length=30, choices=PLAN_OPTS,
                                  verbose_name='Payment plan',
                                  default=PLAN_OPTS[2][0])


class Card(models.Model):
    card_num = models.CharField(max_length=16,
                                verbose_name='Card number')
    billing_addr = models.CharField(max_length=100,
                                    verbose_name='Billing address')
    expires_at = models.DateField(blank=False, verbose_name='Expiry Date')
    cvv = models.CharField(max_length=3, help_text='The 3 digits on '
                                                   'the back of your card')
    holder = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               verbose_name='Card holder', null=True)


def card_post_save(sender, instance, created, *args, **kwargs):
    if created:
        amt = 14.99
        end_date = datetime.datetime.now() + relativedelta(months=1)
        recurrence = 'Monthly'
        if instance.holder.pmt_option == 'Y':
            amt = 149.99
            end_date = datetime.datetime.now() + relativedelta(years=1)
            recurrence = 'Yearly'
        first_pmt = Payment.objects.create(
            amount=amt,
            pmt_method=instance,
            recur=recurrence,
            edate=end_date,
            pmt_status='PA'
        )
        first_pmt.save()


post_save.connect(card_post_save, sender=Card)

PMT_STATUS = [
    ('C', 'Cancelled'),
    ('PA', 'Paid'),
    ('PD', 'Pending')
]


class Payment(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2,
                                 verbose_name = 'Payment amount')
    pmt_method = models.ForeignKey(Card, on_delete=models.DO_NOTHING,
                                   verbose_name = 'Payment method', null=True)
    pmt_date = models.DateTimeField(default=datetime.datetime.now,
                                    verbose_name = 'Payment date')

    recur = models.CharField(max_length=7, verbose_name = 'Recurrence', default='Monthly',
                             help_text='Please choose one of Monthly and Yearly')
    edate = models.DateField(verbose_name='End date', default = date.today)

    #success = models.BooleanField(default=False)
    pmt_status = models.CharField(max_length=2, choices=PMT_STATUS, default=PMT_STATUS[2][0],
                                  verbose_name='Payment status')

    def __str__(self):
        return f'Payment ${self.amount} from card {self.pmt_method.card_num}'
        # return f'Amount: {self.amount}\n' \
        #        f'Card number: {self.pmt_method.card_num}\n' \
        #        f'Date: {self.pmt_date}\n' \
        #        f'Time: {self.pmt_date.strftime("%H:%M:%S")}\n' \
        #        f'Recurrence: {self.recur}\n' \
        #        f'End date: {self.edate}\n' \
        #        f'Payment status: {self.pmt_status}\n' \


def payment_post_save(sender, instance, created, *args, **kwargs):
    if created and instance.pmt_date <= instance.edate:
        new_date = instance.pmt_date
        if instance.recur == 'Monthly':
            new_date += relativedelta(months=1)
        elif instance.recur == 'Yearly':
            new_date += relativedelta(years=1)
        new_pmt = Payment.objects.create(
            amount=instance.amount,
            pmt_method=instance.pmt_method,
            pmt_date=new_date,
            recur=instance.recur,
            edate=instance.edate
        )
        new_pmt.save()


post_save.connect(payment_post_save, sender=Payment)
