# Generated by Django 5.2 on 2025-04-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railway_reservation_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
