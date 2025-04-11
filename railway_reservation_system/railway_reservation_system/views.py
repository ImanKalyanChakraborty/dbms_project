# views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import User, Train, Station, Schedule, Coach, Seat, Passenger, Booking, Ticket, Payment, Route, Availability
from .serializers import (
    UserSerializer, TrainSerializer, StationSerializer, ScheduleSerializer,
    CoachSerializer, SeatSerializer, PassengerSerializer, BookingSerializer,
    TicketSerializer, PaymentSerializer, RouteSerializer, AvailabilitySerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['train_name', 'train_code']
    
    @action(detail=True, methods=['get'])
    def schedules(self, request, pk=None):
        train = self.get_object()
        schedules = Schedule.objects.filter(train=train)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def coaches(self, request, pk=None):
        train = self.get_object()
        coaches = Coach.objects.filter(train=train)
        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data)

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['station_name', 'station_code']

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    def get_queryset(self):
        queryset = Schedule.objects.all()
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        
        if source:
            queryset = queryset.filter(source__station_code=source)
        if destination:
            queryset = queryset.filter(destination__station_code=destination)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        schedule = self.get_object()
        date = request.query_params.get('date', None)
        
        if not date:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        availabilities = Availability.objects.filter(schedule=schedule, journey_date=date)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        queryset = Booking.objects.all()
        user_id = self.request.query_params.get('user', None)
        pnr = self.request.query_params.get('pnr', None)
        
        if user_id:
            queryset = queryset.filter(user=user_id)
        if pnr:
            queryset = queryset.filter(pnr=pnr)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        booking = self.get_object()
        tickets = Ticket.objects.filter(booking=booking)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'CAN'
        booking.save()
        
        # Logic to handle seat availability after cancellation
        schedule = booking.schedule
        journey_date = booking.journey_date
        
        tickets = Ticket.objects.filter(booking=booking)
        coach_types = set()
        
        for ticket in tickets:
            if ticket.seat:
                coach_type = ticket.seat.coach.coach_type
                coach_types.add(coach_type)
        
        for coach_type in coach_types:
            try:
                availability = Availability.objects.get(
                    schedule=schedule,
                    journey_date=journey_date,
                    coach_type=coach_type
                )
                availability.available_seats += len(tickets.filter(seat__coach__coach_type=coach_type))
                if availability.waiting_list > 0:
                    availability.waiting_list -= 1
                availability.save()
            except Availability.DoesNotExist:
                pass
        
        return Response({"status": "Booking cancelled successfully"})

class SearchViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def trains(self, request):
        source = request.query_params.get('source', None)
        destination = request.query_params.get('destination', None)
        date = request.query_params.get('date', None)
        
        if not all([source, destination, date]):
            return Response({"error": "Source, destination and date parameters are required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Find trains that go from source to destination
        schedules = Schedule.objects.filter(source__station_code=source, destination__station_code=destination)
        
        result = []
        for schedule in schedules:
            availabilities = Availability.objects.filter(schedule=schedule, journey_date=date)
            
            if availabilities.exists():
                schedule_data = ScheduleSerializer(schedule).data
                avail_data = AvailabilitySerializer(availabilities, many=True).data
                
                result.append({
                    "schedule": schedule_data,
                    "availability": avail_data
                })
        
        return Response(result)

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    @action(detail=False, methods=['post'])
    def update_availability(self, request):
        """
        Custom endpoint to update availability when booking tickets
        """
        try:
            schedule_id = request.data.get('schedule')
            journey_date = request.data.get('journey_date')
            coach_type = request.data.get('coach_type')
            seats_to_reduce = int(request.data.get('seats_to_reduce', 1))

            # Get the availability record
            availability = get_object_or_404(
                Availability,
                schedule=schedule_id,
                journey_date=journey_date,
                coach_type=coach_type
            )

            # Check if enough seats are available
            if availability.available_seats < seats_to_reduce:
                return Response(
                    {'error': 'Not enough seats available'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update the availability in a transaction
            with transaction.atomic():
                availability.available_seats -= seats_to_reduce
                # If reducing to negative, move to waiting list
                if availability.available_seats < 0:
                    availability.waiting_list += abs(availability.available_seats)
                    availability.available_seats = 0
                availability.save()

            serializer = self.get_serializer(availability)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )