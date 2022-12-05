import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete

PLAN_OPTS = [
    ('M', 'Monthly Plan'),
    ('Y', 'Yearly Plan'),
    ('N', 'Inactive / Cancel plan')
]

PLAN_TYPE = [
    ('M', 'Monthly subscription'),
    ('Y', 'Yearly subscription')
]


class MembershipPlan(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2,
                                verbose_name='Membership price')
    type = models.CharField(max_length=1, choices=PLAN_TYPE,
                            verbose_name='Billing cycle')

    def __str__(self):
        return f'{self.type} plan for {self.price}'


def plan_post_delete(sender, instance, **kwargs):
    users = CustomUser.objects.filter(pmt_option=instance.type)
    if users:
        for user in users:
            payments = Payment.objects.filter(payer=user.username,
                                              pmt_status='PD')
            if payments:
                payments.update(pmt_status='C')
            user.pmt_option='N'
            user.is_subscribed = False


post_delete.connect(plan_post_delete, sender=MembershipPlan)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone_num = models.CharField(max_length=10, verbose_name='Phone',
                                 blank=True)
    avatar = models.ImageField(blank=True, null=True)
    is_subscribed = models.BooleanField(default=False,
                                        verbose_name='Subscription status')
    pmt_option = models.CharField(max_length=1, choices=PLAN_OPTS,
                                  verbose_name='Payment plan',
                                  default=PLAN_OPTS[2][0])
    sub_edate = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.username} + {self.pmt_option} + {self.is_subscribed}'


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

    def __str__(self):
        return f'{self.card_num} and id {self.id}'


def card_post_save(sender, instance, created, *args, **kwargs):
    if created:
        # if holder already has payments associated with the old card, update
        if Payment.objects.filter(payer=instance.holder.username,
                                  pmt_status='PD'):
            if Card.objects.filter(holder=instance.holder).exclude(
                card_num=instance.card_num).exists():
                old_cards = Card.objects.filter(holder=instance.holder).exclude(
                    card_num=instance.card_num)
                pd_pmts = Payment.objects.none()
                if old_cards:
                    for card in old_cards:
                        pd_pmts = pd_pmts | Payment.objects.filter(pmt_method=
                                                card.card_num, pmt_status='PD')
                pd_pmts.update(pmt_method=instance.card_num)
        else:
            amt = MembershipPlan.objects.get(
                type='M').price
            end_date = datetime.date.today() + relativedelta(years=1)
            recurrence = 'Monthly'
            instance.holder.sub_edate = datetime.date.today() \
                                        + relativedelta(months=1)
            instance.holder.save()
            if instance.holder.pmt_option == 'Y':
                recurrence = 'Yearly'
                instance.holder.sub_edate = datetime.date.today() \
                                            + relativedelta(years=1)
                amt = MembershipPlan.objects.get(
                    type='Y').price
            first_pmt = Payment.objects.create(
                amount=amt,
                pmt_method=instance.card_num,
                recur=recurrence,
                edate=end_date,
                pmt_status='PA',
                payer=instance.holder.username,
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
    pmt_method = models.CharField(max_length=16, null=True,
                                  verbose_name='Payment method')
    pmt_date = models.DateTimeField(default=datetime.datetime.now,
                                    verbose_name = 'Payment date')

    recur = models.CharField(max_length=7, verbose_name = 'Recurrence',
                             default='Monthly',
                            help_text='Please choose one of Monthly and Yearly')
    edate = models.DateField(verbose_name='End date',
                             default = datetime.date.today)

    pmt_status = models.CharField(max_length=2, choices=PMT_STATUS,
                                  default=PMT_STATUS[2][0],
                                  verbose_name='Payment status')
    payer = models.CharField(max_length=255, verbose_name="payer's username",
                             null=True)

    def __str__(self):
        return f'Payment ${self.amount} from card {self.pmt_method} on {self.pmt_date}'

    def make_payment(self):
        if datetime.date.today() == self.pmt_date.date() and \
                self.pmt_method is not None:
            self.pmt_status = 'PA'
            self.save()
            return True
        return False


def payment_post_save(sender, instance, created, *args, **kwargs):

    if created and instance.pmt_date.date() < instance.edate:
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
            edate=instance.edate,
            payer=instance.payer,
        )
        new_pmt.save()


post_save.connect(payment_post_save, sender=Payment)
