# Generated by Django 3.2.12 on 2022-02-10 20:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookloaned',
            name='date_borrowed',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
