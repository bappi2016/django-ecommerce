# Generated by Django 2.2.4 on 2019-08-26 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_order_billing_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='phone_no',
            new_name='phone',
        ),
    ]
