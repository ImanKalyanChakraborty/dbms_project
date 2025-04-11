# models.py

from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # In practice, use Django's auth system
    
    def __str__(self):
        return self.username

class Train(models.Model):
    id = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=100)
    train_code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.train_name} ({self.train_code})"

class Station(models.Model):
    id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=100)
    station_code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.station_name} ({self.station_code})"

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='schedules')
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    run_days = models.CharField(max_length=50)  # Can store comma-separated days or use a separate model
    fare = models.FloatField()
    
    def __str__(self):
        return f"{self.train} - {self.source} to {self.destination}"

class Coach(models.Model):
    COACH_TYPES = [
        ('SL', 'Sleeper'),
        ('AC', 'AC'),
        ('GN', 'General'),
        ('1A', '1st AC'),
        ('2A', '2nd AC'),
        ('3A', '3rd AC'),
        ('CC', 'Chair Car'),
    ]
    
    id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='coaches')
    coach_type = models.CharField(max_length=2, choices=COACH_TYPES)
    coach_number = models.CharField(max_length=10)
    total_seats = models.IntegerField()
    
    class Meta:
        unique_together = ('train', 'coach_number')
        
    def __str__(self):
        return f"{self.train} - {self.coach_type}{self.coach_number}"

class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ('coach', 'seat_number')
        
    def __str__(self):
        return f"{self.coach} - Seat {self.seat_number}"

class Passenger(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('CNF', 'Confirmed'),
        ('WL', 'Waiting List'),
        ('RAC', 'Reservation Against Cancellation'),
        ('CAN', 'Cancelled'),
    ]
    
    id = models.AutoField(primary_key=True)
    pnr = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=10, unique=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='bookings')
    journey_date = models.DateField()
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='CNF')
    
    def __str__(self):
        return f"PNR: {self.pnr}"

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='tickets')
    # seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    
    def __str__(self):
        return f"{self.booking.pnr} - {self.passenger.name}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('UPI', 'UPI'),
        ('NB', 'Net Banking'),
        ('WL', 'Wallet'),
    ]
    
    STATUS_CHOICES = [
        ('S', 'Success'),
        ('F', 'Failed'),
        ('P', 'Pending'),
    ]
    
    id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    def __str__(self):
        return f"{self.booking.pnr} - {self.amount}"

class Route(models.Model):
    id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes')
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    day = models.IntegerField(default=1)  # Day of journey when this station is reached
    sequence = models.IntegerField()  # Order of station in the route
    distance = models.IntegerField()  # Distance from origin in km
    
    class Meta:
        unique_together = ('train', 'station')
        
    def __str__(self):
        return f"{self.train} - {self.station} (Day {self.day})"

class Availability(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='availabilities')
    journey_date = models.DateField()
    coach_type = models.CharField(max_length=2, choices=Coach.COACH_TYPES)
    available_seats = models.IntegerField()
    waiting_list = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('schedule', 'journey_date', 'coach_type')
        
    def __str__(self):
        return f"{self.schedule} - {self.journey_date} ({self.coach_type})"