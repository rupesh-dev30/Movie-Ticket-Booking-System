from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Show, Booking

# Simple user serializer for signup
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'duration_minutes')

class ShowSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Show
        fields = ('id', 'movie', 'screen_name', 'date_time', 'total_seats')

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    show = ShowSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'user', 'show', 'seat_number', 'status', 'created_at')

# serializer used to accept seat number for booking
class CreateBookingSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField(min_value=1)
