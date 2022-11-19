# Generated by Django 4.1.2 on 2022-11-16 21:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_payment_pmt_date_alter_payment_pmt_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='pmt_option',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payer',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='success',
        ),
        migrations.AddField(
            model_name='customuser',
            name='pmt_option',
            field=models.CharField(choices=[('M', 'Monthly Plan $14.99 per month'), ('Y', 'Yearly Plan $149.99 per year'), ('N', 'Inactive / Cancel plan')], default='N', max_length=30, verbose_name='Payment plan'),
        ),
        migrations.AddField(
            model_name='payment',
            name='edate',
            field=models.DateField(default=datetime.date.today, verbose_name='End date'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pmt_status',
            field=models.CharField(choices=[('C', 'Cancelled'), ('PA', 'Paid'), ('PD', 'Pending')], default='PD', max_length=2, verbose_name='Payment status'),
        ),
        migrations.AddField(
            model_name='payment',
            name='recur',
            field=models.CharField(default='Monthly', help_text='Please choose one of Monthly and Yearly', max_length=7, verbose_name='Recurrence'),
        ),
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.CharField(help_text='The 3 digits on the back of your card', max_length=3),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_subscribed',
            field=models.BooleanField(default=False, verbose_name='Subscription status'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pmt_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Payment date'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pmt_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.card', verbose_name='Payment method'),
        ),
    ]
