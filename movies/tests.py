from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from rest_framework_simplejwt.tokens import RefreshToken
import datetime

class BookingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create movie and show
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name='Screen 1',
            date_time=datetime.datetime(2025,10,6,20,0),
            total_seats=5
        )

        # Generate JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_booking_seat(self):
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['seat_number'], 1)

    def test_double_booking(self):
        # First booking
        self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        # Second booking same seat
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Seat is already booked', response.data['detail'])
