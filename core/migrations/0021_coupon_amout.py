# Generated by Django 2.2.4 on 2019-08-29 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amout',
            field=models.FloatField(default=5.0),
        ),
    ]
