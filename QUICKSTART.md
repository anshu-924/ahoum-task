# 🚀 Quick Start Guide - Sessions Marketplace

## One Command Setup

```bash
docker-compose up --build
```

That's it! Wait 30-60 seconds, then open http://localhost

## First Time Setup

1. **Clone & Configure**
```bash
git clone <your-repo>
cd ahoum
cp .env.example .env
# Edit .env if needed (optional for demo)
```

2. **Start Application**
```bash
docker-compose up --build
```

3. **Access Application**
- Frontend: http://localhost
- Admin: http://localhost/admin (admin/admin123)
- API Docs: http://localhost/swagger

## Demo Flow (2 minutes)

### As Student
1. Click "Login" → Select "Student" → "Demo Login"
2. Browse sessions on home page
3. Click session → "View Details" → Fill form → "Book Now"
4. Go to "Dashboard" to see booking

### As Tutor
1. Click "Login" → Select "Tutor" → "Demo Login"
2. Click "Create New Session"
3. Fill details (Meditation, Yoga, etc.) → "Create Session"
4. Go to "Creator Dashboard" to see sessions and bookings

## What You Get

✅ Full-stack application (React + Django)
✅ OAuth authentication with JWT
✅ Role-based access (Student/Tutor)
✅ Session catalog with booking
✅ User & Creator dashboards
✅ PostgreSQL database
✅ Nginx reverse proxy
✅ Docker containers for everything

## Tech Stack

- **Frontend**: React 18 + React Router
- **Backend**: Django REST Framework
- **Database**: PostgreSQL 15
- **Proxy**: Nginx
- **Container**: Docker Compose

## Containers Running

1. `sessions_db` - PostgreSQL (port 5432)
2. `sessions_backend` - Django API (port 8000)
3. `sessions_frontend` - React App (port 3000)
4. `sessions_nginx` - Reverse Proxy (port 80)

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop all
docker-compose down

# Restart
docker-compose restart

# Rebuild specific service
docker-compose up --build frontend
```

## Troubleshooting

**Port 80 in use?**
```bash
# Change nginx port in docker-compose.yml
ports:
  - "8080:80"  # Use 8080 instead
```

**Want to reset everything?**
```bash
docker-compose down -v
docker-compose up --build
```

**Frontend not loading?**
```bash
docker logs sessions_frontend
docker logs sessions_nginx
```

## Next Steps

- Read [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) for details
- See [FRONTEND_SETUP.md](FRONTEND_SETUP.md) for frontend info
- Check [API_EXAMPLES.md](API_EXAMPLES.md) for API testing

## 🎉 You're Ready!

Open http://localhost and start exploring!
