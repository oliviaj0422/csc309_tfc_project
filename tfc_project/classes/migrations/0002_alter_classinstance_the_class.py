# Generated by Django 4.1.3 on 2022-12-08 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classinstance',
            name='the_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.class', unique=True),
        ),
    ]
