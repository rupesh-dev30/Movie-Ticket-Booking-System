from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from rest_framework.test import APIClient

class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(movie=self.movie, screen_name='Screen 1', date_time='2025-10-10T10:00', total_seats=5)
        self.client = APIClient()
        response = self.client.post('/api/login/', {'username':'testuser','password':'pass'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_book_seat_success(self):
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

    def test_double_booking(self):
        self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1})
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1})
        self.assertEqual(response.status_code, 400)

    def test_overbooking(self):
        for i in range(1, 6):
            self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': i})
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 6})
        self.assertEqual(response.status_code, 400)

    def test_cancel_booking(self):
        res = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1})
        booking_id = res.data['id']
        cancel_res = self.client.post(f'/api/bookings/{booking_id}/cancel/')
        self.assertEqual(cancel_res.status_code, 200)
        booking = Booking.objects.get(id=booking_id)
        self.assertEqual(booking.status, 'cancelled')
