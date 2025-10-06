from django.urls import path
from .views import SignupView, MovieListView, MovieShowsView, BookSeatView, CancelBookingView, MyBookingsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # auth
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # movies/shows
    path('movies/', MovieListView.as_view(), name='movies_list'),
    path('movies/<int:movie_id>/shows/', MovieShowsView.as_view(), name='movie_shows'),

    # booking actions
    path('shows/<int:show_id>/book/', BookSeatView.as_view(), name='book_seat'),
    path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='cancel_booking'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
]
