# Generated by Django 3.2.12 on 2022-02-10 19:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220210_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloaned',
            name='date_borrowed',
            field=models.DateField(default=datetime.datetime(2022, 2, 10, 19, 0, 7, 397772, tzinfo=utc)),
        ),
    ]
