# Movie Ticket Booking System

## Overview
This is a backend system for a Movie Ticket Booking application built with Django & Django REST Framework (DRF).  
It supports user signup/login, movie/show management, seat booking, cancellation, and JWT authentication.

## Tech Stack
- Python 3
- Django
- Django REST Framework
- djangorestframework-simplejwt (JWT Auth)
- drf-yasg (Swagger API docs)
- SQLite (default DB)

## Features
- Signup & Login with JWT
- List Movies & Shows
- Book seats for a show
- Cancel bookings
- View your bookings
- Swagger API documentation

## Setup Instructions

### 1. Clone the repository
```bash
git clone <YOUR_REPO_URL>
cd ticketing
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Activate the environment
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (optional, for admin access)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

### 7. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/signup/ | POST | Register a new user |
| /api/login/ | POST | Get JWT tokens |
| /api/movies/ | GET | List all movies |
| /api/movies/<id>/shows/ | GET | List shows for a movie |
| /api/shows/<id>/book/ | POST | Book a seat (JWT required) |
| /api/my-bookings/ | GET | List logged-in user's bookings (JWT required) |
| /api/bookings/<id>/cancel/ | POST | Cancel a booking (JWT required) |

### 8. Swagger Documentation
```bash
http://127.0.0.1:8000/swagger/
Use the Authorize button to provide JWT token for protected endpoints.
```

### 9. Running Tests
- To ensure booking logic works correctly:
```bash
python manage.py test
```