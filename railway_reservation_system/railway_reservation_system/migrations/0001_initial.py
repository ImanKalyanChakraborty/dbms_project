# Generated by Django 5.2 on 2025-04-07 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pnr', models.CharField(max_length=10, unique=True)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('journey_date', models.DateField()),
                ('total_fare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('CNF', 'Confirmed'), ('WL', 'Waiting List'), ('RAC', 'Reservation Against Cancellation'), ('CAN', 'Cancelled')], default='CNF', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coach_type', models.CharField(choices=[('SL', 'Sleeper'), ('AC', 'AC'), ('GN', 'General'), ('1A', '1st AC'), ('2A', '2nd AC'), ('3A', '3rd AC'), ('CC', 'Chair Car')], max_length=2)),
                ('coach_number', models.CharField(max_length=10)),
                ('total_seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=15)),
                ('id_proof', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('run_days', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=100)),
                ('station_code', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=100)),
                ('train_code', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('CC', 'Credit Card'), ('DC', 'Debit Card'), ('UPI', 'UPI'), ('NB', 'Net Banking'), ('WL', 'Wallet')], max_length=4)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('S', 'Success'), ('F', 'Failed'), ('P', 'Pending')], default='P', max_length=1)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='railway_reservation_system.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='railway_reservation_system.schedule'),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seat_number', models.CharField(max_length=10)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='railway_reservation_system.coach')),
            ],
            options={
                'unique_together': {('coach', 'seat_number')},
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='railway_reservation_system.station'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='railway_reservation_system.station'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='railway_reservation_system.booking')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='railway_reservation_system.passenger')),
                ('seat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='railway_reservation_system.seat')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='railway_reservation_system.train'),
        ),
        migrations.AddField(
            model_name='coach',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coaches', to='railway_reservation_system.train'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='railway_reservation_system.user'),
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('journey_date', models.DateField()),
                ('coach_type', models.CharField(choices=[('SL', 'Sleeper'), ('AC', 'AC'), ('GN', 'General'), ('1A', '1st AC'), ('2A', '2nd AC'), ('3A', '3rd AC'), ('CC', 'Chair Car')], max_length=2)),
                ('available_seats', models.IntegerField()),
                ('waiting_list', models.IntegerField(default=0)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='railway_reservation_system.schedule')),
            ],
            options={
                'unique_together': {('schedule', 'journey_date', 'coach_type')},
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('arrival_time', models.TimeField(blank=True, null=True)),
                ('departure_time', models.TimeField(blank=True, null=True)),
                ('day', models.IntegerField(default=1)),
                ('sequence', models.IntegerField()),
                ('distance', models.IntegerField()),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='railway_reservation_system.station')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='railway_reservation_system.train')),
            ],
            options={
                'unique_together': {('train', 'station')},
            },
        ),
        migrations.CreateModel(
            name='Fare',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coach_type', models.CharField(choices=[('SL', 'Sleeper'), ('AC', 'AC'), ('GN', 'General'), ('1A', '1st AC'), ('2A', '2nd AC'), ('3A', '3rd AC'), ('CC', 'Chair Car')], max_length=2)),
                ('base_fare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_fares', to='railway_reservation_system.station')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_fares', to='railway_reservation_system.station')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fares', to='railway_reservation_system.train')),
            ],
            options={
                'unique_together': {('train', 'source', 'destination', 'coach_type')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='coach',
            unique_together={('train', 'coach_number')},
        ),
    ]
