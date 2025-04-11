# serializers.py

from rest_framework import serializers
from .models import User, Train, Station, Schedule, Coach, Seat, Passenger, Booking, Ticket, Payment, Route, Availability

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'station_name', 'station_code']

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ['id', 'train_name', 'train_code']

class ScheduleSerializer(serializers.ModelSerializer):
    train_detail = TrainSerializer(source='train', read_only=True)
    source_detail = StationSerializer(source='source', read_only=True)
    destination_detail = StationSerializer(source='destination', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'train', 'train_detail', 'source', 'source_detail', 
            'destination', 'destination_detail', 'departure_time', 
            'arrival_time', 'run_days', 'fare'
        ]

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'train', 'coach_type', 'coach_number', 'total_seats']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'coach', 'seat_number']

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'name', 'age', 'gender', 'phone']

class BookingSerializer(serializers.ModelSerializer):
    schedule_detail = ScheduleSerializer(source='schedule', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'pnr', 'user', 'schedule', 'schedule_detail', 
            'journey_date', 'total_fare', 'status'
        ]

class TicketSerializer(serializers.ModelSerializer):
    passenger_detail = PassengerSerializer(source='passenger', read_only=True)
    seat_detail = SeatSerializer(source='seat', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'booking', 'passenger', 'passenger_detail', 'seat_detail']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'payment_date', 
            'payment_method', 'transaction_id', 'status'
        ]

class RouteSerializer(serializers.ModelSerializer):
    station_detail = StationSerializer(source='station', read_only=True)
    
    class Meta:
        model = Route
        fields = [
            'id', 'train', 'station', 'station_detail', 'arrival_time', 
            'departure_time', 'day', 'sequence', 'distance'
        ]

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = [
            'id', 'schedule', 'journey_date', 'coach_type', 
            'available_seats', 'waiting_list'
        ]