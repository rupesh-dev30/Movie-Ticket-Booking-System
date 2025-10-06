from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Movie, Show, Booking
from .serializers import MovieSerializer, ShowSerializer, BookingSerializer, SignupSerializer, CreateBookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError
from django.db.models import Count
from .permissions import IsOwnerOrReadOnly
import time

# Signup
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

# List movies
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.AllowAny,)

# List shows for a movie
class MovieShowsView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Show.objects.filter(movie_id=movie_id)

# Book seat view
class BookSeatView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, show_id):
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seat_number = serializer.validated_data['seat_number']
        user = request.user
        show = get_object_or_404(Show, id=show_id)

        # Validate seat number in range
        if seat_number < 1 or seat_number > show.total_seats:
            return Response({"detail": "seat_number outside valid range."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to create booking in a transaction. Use DB constraint + retry loop to handle concurrency.
        max_retries = 5
        for attempt in range(max_retries):
            try:
                with transaction.atomic():
                    # Prevent overbooking: count currently active bookings for show
                    booked_count = Booking.objects.filter(show=show, status='booked').count()
                    if booked_count >= show.total_seats:
                        return Response({"detail": "Show is fully booked."}, status=status.HTTP_400_BAD_REQUEST)

                    # Create booking object; unique_together prevents double seat booking
                    booking = Booking.objects.create(user=user, show=show, seat_number=seat_number, status='booked')
                    out = BookingSerializer(booking).data
                    return Response(out, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # Happens if seat already booked (unique constraint) or race condition
                # If seat was just taken -> inform user or retry small sleep and retry
                if 'unique' in str(e).lower() or 'unique constraint' in str(e).lower():
                    return Response({"detail": "Seat is already booked."}, status=status.HTTP_400_BAD_REQUEST)
                # otherwise retry a few times
                if attempt < max_retries - 1:
                    time.sleep(0.1)  # short wait then retry
                    continue
                return Response({"detail": "Could not complete booking. Try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Cancel booking
class CancelBookingView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        # security: user can only cancel their own booking
        if booking.user != request.user:
            return Response({"detail": "Cannot cancel someone else's booking."}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == 'cancelled':
            return Response({"detail": "Booking already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            booking.status = 'cancelled'
            booking.save()
        return Response({"detail": "Booking cancelled."}, status=status.HTTP_200_OK)

# List my bookings
class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')
