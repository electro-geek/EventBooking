# 🚀 Event Booking System API Testing Guide

The API is deployed at: `https://event-booking-three.vercel.app/`

This guide provides `curl` commands to test the core features of the system.

---

## 1. Authentication & User Management

### A. Register as an Organizer
**Purpose:** Create a user with permissions to create and manage events.
```bash
curl -X 'POST' \
  'https://event-booking-three.vercel.app/api/v1/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "organizer@example.com",
  "full_name": "Event Master",
  "role": "organizer",
  "password": "securepassword123"
}'
```

### B. Register as a Customer
**Purpose:** Create a user who can browse and book events.
```bash
curl -X 'POST' \
  'https://event-booking-three.vercel.app/api/v1/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "customer@example.com",
  "full_name": "John Doe",
  "role": "customer",
  "password": "customerpassword123"
}'
```

### C. Login
**Purpose:** Obtain a JWT Token for authorized requests.
```bash
curl -X 'POST' \
  'https://event-booking-three.vercel.app/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=organizer@example.com&password=securepassword123'
```
*Take the `access_token` from the response and export it:* `export TOKEN="your_token_here"`

---

## 2. Event Management (Organizer Required)

### A. Create an Event
**Purpose:** Add a new event to the platform.
```bash
curl -X 'POST' \
  'https://event-booking-three.vercel.app/api/v1/events/' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Tech Conference 2026",
  "description": "The biggest tech event of the year",
  "location": "San Francisco",
  "start_time": "2026-06-01T10:00:00",
  "end_time": "2026-06-01T18:00:00",
  "total_slots": 50
}'
```

### B. List All Events
**Purpose:** Browse all available events (No auth required).
```bash
curl -X 'GET' \
  'https://event-booking-three.vercel.app/api/v1/events/' \
  -H 'accept: application/json'
```

### C. Update an Event
**Purpose:** Modify event details. This triggers a background notification to all booked customers.
```bash
curl -X 'PUT' \
  'https://event-booking-three.vercel.app/api/v1/events/1' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Tech Conference 2026 - Updated",
  "total_slots": 100
}'
```

---

## 3. Ticketing & Bookings (Customer Required)

### A. Book a Ticket
**Purpose:** Reserve a spot for an event. If slots are full, user is added to the Waitlist.
```bash
curl -X 'POST' \
  'https://event-booking-three.vercel.app/api/v1/bookings/' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "event_id": 1,
  "ticket_quantity": 1
}'
```

### B. View My Bookings
**Purpose:** See all tickets booked by the current user.
```bash
curl -X 'GET' \
  'https://event-booking-three.vercel.app/api/v1/bookings/my-bookings' \
  -H "Authorization: Bearer $TOKEN"
```

---

## 4. Documentation
You can also access the interactive **Swagger UI** to test these endpoints directly in the browser:
👉 [https://event-booking-three.vercel.app/docs](https://event-booking-three.vercel.app/docs)
