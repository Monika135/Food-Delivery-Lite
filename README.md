# Food-Delivery-Lite

Small Django project for food delivery bookings with REST API + WebSocket (Channels) features.

## Requirements
- Python 3.10+ (adjust if repo requires different version)
- pip
- (optional) daphne for ASGI production testing

## Quick start (Windows)
1. Clone
   git clone <repo-url> Food-Delivery-Lite
   cd Food-Delivery-Lite

2. Create & activate virtual environment
   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Apply migrations
   python manage.py migrate

5. Create superuser (for admin)
   python manage.py createsuperuser

6. Run local server
   python manage.py runserver

7. (Optional) Run ASGI with daphne
   pip install daphne
   daphne -p 8000 food_delivery.asgi:application

## Run tests
python manage.py test

## Project layout (important files)
- manage.py — Django entrypoint
- requirements.txt — Python dependencies
- food_delivery/
  - settings.py — main settings (DB, AUTH_USER_MODEL, REST_FRAMEWORK, SIMPLE_JWT, ASGI_APPLICATION)
  - asgi.py — Channels / ASGI configuration
  - urls.py — top-level URL routes and template views
- bookings/
  - models.py — Product, BookingStatus, Booking (domain models)
  - admin.py — registers Product, BookingStatus, Booking in admin
  - views.py, serializers.py — API endpoints
  - consumers.py, routing.py, middleware.py — WebSocket (Channels) handlers + JWT middleware
  - tests.py — unit tests
- users/ — custom user model (AUTH_USER_MODEL)
- templates/ — front-end pages (login, chat, dashboard)
- db.sqlite3 — default SQLite DB (after migrations)

## WebSocket / Auth notes
- The project uses Django Channels; WebSocket routes are defined in bookings.routing and wired in asgi.py.
- WebSocket auth is implemented via JWT middleware (inspect bookings/middleware.py). Client sockets must send a valid JWT as expected by that middleware.
- REST authentication uses `rest_framework_simplejwt` (see settings.SIMPLE_JWT).

## Environment & security
- settings.py currently contains DEBUG=True and a local SECRET_KEY. Replace with environment variables in production.
- Recommended environment variables:
  - SECRET_KEY
  - DEBUG (False in production)
  - DATABASE_URL (if switching from sqlite)

## Admin
- Access /admin after creating a superuser. Bookings and products are registered in bookings/admin.py.
