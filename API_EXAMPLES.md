# API Testing Examples

## Authentication

### OAuth Login (Google)
```bash
curl -X POST http://localhost/api/auth/oauth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "google",
    "access_token": "your-google-access-token",
    "role": "user"
  }'
```

### OAuth Login (GitHub)
```bash
curl -X POST http://localhost/api/auth/oauth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "github",
    "access_token": "your-github-access-token",
    "role": "creator"
  }'
```

### Refresh Token
```bash
curl -X POST http://localhost/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your-refresh-token"
  }'
```

## Sessions

### List Sessions (Public)
```bash
curl http://localhost/api/sessions/
```

### Get Session Detail
```bash
curl http://localhost/api/sessions/1/
```

### Create Session (Creator only)
```bash
curl -X POST http://localhost/api/sessions/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Web Development",
    "description": "Learn Django and REST Framework from scratch",
    "category": "Programming",
    "duration_minutes": 60,
    "price": "49.99",
    "currency": "USD",
    "max_attendees": 10,
    "location": "Online",
    "session_type": "online",
    "status": "published"
  }'
```

### Update Session
```bash
curl -X PUT http://localhost/api/sessions/1/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python Web Development",
    "price": "59.99"
  }'
```

### My Sessions (Creator)
```bash
curl http://localhost/api/sessions/my_sessions/ \
  -H "Authorization: Bearer your-access-token"
```

## Bookings

### Create Booking
```bash
curl -X POST http://localhost/api/bookings/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "session": 1,
    "booking_date": "2025-01-15T10:00:00Z",
    "attendees_count": 2,
    "user_notes": "Looking forward to this!"
  }'
```

### List My Bookings
```bash
curl http://localhost/api/bookings/my_bookings/ \
  -H "Authorization: Bearer your-access-token"
```

### Get Active Bookings
```bash
curl http://localhost/api/bookings/active/ \
  -H "Authorization: Bearer your-access-token"
```

### Confirm Booking (Creator)
```bash
curl -X POST http://localhost/api/bookings/1/confirm/ \
  -H "Authorization: Bearer your-access-token"
```

### Cancel Booking
```bash
curl -X POST http://localhost/api/bookings/1/cancel/ \
  -H "Authorization: Bearer your-access-token"
```

## Dashboards

### User Dashboard
```bash
curl http://localhost/api/dashboard/user/ \
  -H "Authorization: Bearer your-access-token"
```

### Creator Dashboard
```bash
curl http://localhost/api/dashboard/creator/ \
  -H "Authorization: Bearer your-access-token"
```

## Profile

### Get My Profile
```bash
curl http://localhost/api/users/me/ \
  -H "Authorization: Bearer your-access-token"
```

### Update Profile
```bash
curl -X PUT http://localhost/api/users/update_profile/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Full-stack developer",
    "phone": "+1234567890"
  }'
```

## Payment (Bonus)

### Create Payment Intent
```bash
curl -X POST http://localhost/api/payment/create-intent/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 1
  }'
```

### Confirm Payment
```bash
curl -X POST http://localhost/api/payment/confirm/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_intent_id": "pi_xxx"
  }'
```

## Storage (Bonus)

### Upload File
```bash
curl -X POST http://localhost/api/storage/upload/ \
  -H "Authorization: Bearer your-access-token" \
  -F "file=@/path/to/image.jpg" \
  -F "folder=sessions"
```

### Delete File
```bash
curl -X DELETE http://localhost/api/storage/delete/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "sessions/filename.jpg"
  }'
```

## Notes

- Replace `your-access-token` with actual JWT access token
- Replace `localhost` with your domain in production
- All authenticated endpoints require `Authorization: Bearer <token>` header
- Times should be in ISO 8601 format with timezone
