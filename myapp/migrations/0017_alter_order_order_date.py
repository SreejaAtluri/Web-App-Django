# Generated by Django 4.0.6 on 2022-08-14 01:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 14, 1, 27, 25, 191004, tzinfo=utc)),
        ),
    ]
