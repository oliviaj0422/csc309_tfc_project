# Generated by Django 4.1.2 on 2022-11-14 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='billing_addr',
            field=models.CharField(max_length=100, verbose_name='Billing Address'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_num',
            field=models.CharField(max_length=12, verbose_name='Card Number'),
        ),
        migrations.AlterField(
            model_name='card',
            name='expires_at',
            field=models.DateField(verbose_name='Expiry Date'),
        ),
        migrations.AlterField(
            model_name='card',
            name='pmt_option',
            field=models.CharField(choices=[('MONTHLY', 'Monthly Plan'), ('YEARLY', 'Yearly Plan')], max_length=30, verbose_name='Payment Plan'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_num',
            field=models.CharField(max_length=10, verbose_name='Phone'),
        ),
    ]
