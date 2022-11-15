from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL
from datetime import datetime
import recurrence
from dateutil.relativedelta import relativedelta
from recurrence.fields import RecurrenceField

PAYMENT_PLAN = [
    ('M', 'Monthly Plan $14.99 per month'),
    ('Y', 'Yearly Plan $149.99 per year')
]


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone_num = models.CharField(max_length=10, verbose_name='Phone',
                                 blank=True)
    avatar = models.ImageField(blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)


class Card(models.Model):
    card_num = models.CharField(max_length=16,
                                verbose_name='Card Number')
    billing_addr = models.CharField(max_length=100,
                                    verbose_name='Billing Address')
    expires_at = models.DateField(blank=False, verbose_name='Expiry Date')
    cvv = models.CharField(max_length=3)
    pmt_option = models.CharField(max_length=30, choices=PAYMENT_PLAN,
                                  verbose_name='Payment Plan')
    holder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
                               verbose_name='Card holder')


# class Payment(models.Model):
#     amount = models.DecimalField(max_digits=5, decimal_places=2,
#                                  verbose_name = 'Payment amount', blank=False)
#     pmt_method = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True,
#                                    blank=False)
#     pmt_date = models.DateTimeField(auto_now_add=True,
#                                     verbose_name = 'Payment date', blank=False)
#     paid_for = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
#                                  blank=False)
#     # if pmt_option == 'MONTHLY':
#     #     myrule = recurrence.Rule(
#     #         recurrence.MONTHLY
#     #     )
#     # else:
#     myrule = recurrence.Rule(
#         recurrence.YEARLY
#     )
#     pattern = recurrence.Recurrence(
#         dtstart=datetime.now(),
#         dtend=datetime.now() + relativedelta(years=15),
#         rrules=[myrule, ]
#     )
#     recurrences = RecurrenceField(null=True)
