# Generated by Django 3.2.12 on 2022-02-10 19:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_bookloaned_date_borrowed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloaned',
            name='date_borrowed',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
