# Frontend README

## Overview
React-based frontend for Sessions Marketplace application.

## Features
- OAuth authentication (Google & GitHub)
- Session browsing and booking
- User dashboard (view bookings, manage profile)
- Creator dashboard (create sessions, view stats)
- Responsive design with black, grey, white color scheme

## Pages
- **Home** - Browse sessions catalog
- **Login** - OAuth authentication with role selection
- **Session Detail** - View session details and book
- **User Dashboard** - View bookings and profile
- **Creator Dashboard** - Manage sessions and bookings
- **Profile** - Edit user profile
- **Create Session** - Create new session (creator only)

## Development

### Local Setup
```bash
cd frontend
npm install
npm start
```

### Environment Variables
Copy `.env.example` to `.env` and configure:
```
REACT_APP_API_URL=/api
```

## Docker Deployment
The frontend is automatically built and deployed with docker-compose:

```bash
docker-compose up --build
```

Access the app at http://localhost

## API Integration
The frontend communicates with the Django backend via:
- Base URL: `/api` (proxied through nginx)
- Authentication: JWT tokens in localStorage
- Auto token refresh on 401 errors

## Tech Stack
- React 18
- React Router v6
- Axios for API calls
- CSS3 (no external UI libraries for simplicity)
