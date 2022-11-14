from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL
from datetime import datetime
import recurrence
from dateutil.relativedelta import relativedelta
from recurrence.fields import RecurrenceField

PAYMENT_PLAN = [
    ('MONTHLY', 'Monthly Plan'),
    ('YEARLY', 'Yearly Plan')
]


class Card(models.Model):
    card_num = models.CharField(max_length=12, blank=False)
    billing_addr = models.CharField(max_length=100, blank=False)
    expires_at = models.DateField(blank=False)
    cvv = models.CharField(max_length=3, blank=False)
    pmt_option = models.CharField(max_length=30, choices=PAYMENT_PLAN,
                                  blank=False)
    # if pmt_option == 'MONTHLY':
    #     myrule = recurrence.Rule(
    #         recurrence.MONTHLY
    #     )
    # else:
    myrule = recurrence.Rule(
        recurrence.YEARLY
    )
    pattern = recurrence.Recurrence(
        dtstart=datetime.now(),
        dtend=datetime.now() + relativedelta(years=15),
        rrules=[myrule, ]
    )
    recurrences = RecurrenceField(null=True)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone_num = models.CharField(max_length=10)
    avatar = models.ImageField()
    is_subscribed = models.BooleanField(default=False)
    card_info = models.ForeignKey(Card, on_delete=SET_NULL, null=True)


    #USERNAME_FIELD = 'email'

