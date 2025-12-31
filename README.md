# Sessions Marketplace - Full Stack Application




























































































































































































- No external UI libraries (custom CSS for simplicity)- `axios` - HTTP client- `react-router-dom` - Routing- `react` - UI library## Dependencies- `npm eject` - Eject from Create React App- `npm test` - Run tests- `npm build` - Build for production- `npm start` - Start development server## Available ScriptsThe build folder will contain optimized production files.```npm run buildcd frontend```bash## Building for Production- Use Demo Login to create new session- Refresh tokens expire after 7 days- JWT tokens expire after 1 day### Session expired- Check redirect URIs match exactly- Verify OAuth credentials in backend `.env`- Use Demo Login for testing### OAuth not working- Verify API_URL in `.env`- Check browser console for errors- Verify backend is running### API calls failing- Verify frontend container is built: `docker-compose build frontend`- Check nginx logs: `docker logs sessions_nginx`- Check if nginx container is running: `docker ps`### Frontend not loading## Troubleshooting- **Components**: Reusable cards, buttons, forms- **Layout**: Responsive grid system- **Typography**: System fonts (Segoe UI, Roboto, etc.)- **Colors**: Black (#000000), Grey (#666666), White (#FFFFFF)The app uses a minimalist design with:## Design- `GET /api/dashboard/creator/` - Creator dashboard- `GET /api/dashboard/user/` - User dashboard- `GET /api/bookings/my_bookings/` - User bookings- `POST /api/bookings/` - Create booking- `GET /api/sessions/:id/` - Session detail- `POST /api/sessions/` - Create session- `GET /api/sessions/` - List sessions- `PUT /api/users/update_profile/` - Update profile- `GET /api/users/me/` - Get current user- `POST /api/auth/token/refresh/` - Refresh token- `POST /api/auth/oauth/login/` - OAuth login### API Endpoints Used- **Error Handling**: User-friendly error messages- **Token Refresh**: Automatic refresh on 401 errors- **Authentication**: JWT tokens stored in localStorage- **Base URL**: `/api` (proxied through Nginx in production)The frontend communicates with the backend via:## API Integration7. View your sessions and bookings in dashboard6. Fill session details and submit5. Click "Create New Session"4. Go to "Creator Dashboard"3. Click "Demo Login"2. Select "Tutor" role1. Go to http://localhost/login### As a Tutor8. Go to "Dashboard" to view your bookings7. Fill booking form and submit6. Click "View Details" on any session5. Browse sessions on home page4. Click "Demo Login"3. Select "Student" role2. Click "Get Started" or "Login"1. Go to http://localhost### As a Student## Demo Flow   ```   GITHUB_OAUTH_CLIENT_SECRET=your-client-secret   GITHUB_OAUTH_CLIENT_ID=your-client-id   ```4. Copy Client ID and add to backend `.env`:3. Authorization callback URL: `http://localhost/api/auth/oauth/callback/github/`2. Create new OAuth App1. Go to [GitHub Developer Settings](https://github.com/settings/developers)### GitHub OAuth   ```   GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret   GOOGLE_OAUTH_CLIENT_ID=your-client-id   ```6. Copy Client ID and add to backend `.env`:5. Add authorized redirect URI: `http://localhost/api/auth/oauth/callback/google/`4. Create OAuth 2.0 credentials3. Enable Google+ API2. Create a project1. Go to [Google Cloud Console](https://console.cloud.google.com/)### Google OAuthTo enable real OAuth authentication:## OAuth Setup (Optional)7. **Create Session** - Create new session (tutors only)6. **Profile** - Edit user information5. **Creator Dashboard** - Manage sessions and bookings4. **User Dashboard** - View bookings and profile3. **Session Detail** - View session info and book2. **Login** - Select role (Student/Tutor) and login1. **Home** - Browse sessions catalog with category filters### Pages- **Tutor (Creator)**: Create sessions, manage bookings, view stats- **Student (User)**: Browse sessions, make bookings, view dashboard### User Roles- **OAuth Login**: Configure Google/GitHub OAuth credentials (see OAuth Setup below)- **Demo Login**: Use the "Demo Login" button for quick testing### Authentication## FeaturesThe app will open at http://localhost:3000```npm start```bash### 3. Start Development Server```REACT_APP_API_URL=http://localhost:8000/api```Edit `.env`:```cp .env.example .env```bash### 2. Configure Environment```npm installcd frontend```bash### 1. Install DependenciesIf you want to run the frontend locally for development:## Local Development (Without Docker)Access the app at http://localhost```docker-compose up --build# From project root```bashThe easiest way to run the frontend is with Docker Compose (already configured):## Quick Start with DockerA comprehensive full-stack web application for a Sessions Marketplace with OAuth authentication, JWT tokens, PostgreSQL database, and Docker deployment. Built with React frontend and Django REST Framework backend.

## 🎯 Features

### Core Features
- ✅ **OAuth Authentication** (Google & GitHub)
- ✅ **JWT Token Management** with refresh tokens
- ✅ **Role-Based Access Control** (Student/User & Tutor/Creator roles)
- ✅ **Sessions Management** - Create, update, and manage sessions
- ✅ **Booking System** - Book sessions with status tracking
- ✅ **User Dashboard** - View bookings and profile
- ✅ **Creator Dashboard** - Manage sessions and view bookings
- ✅ **PostgreSQL Database** with optimized queries
- ✅ **Docker Deployment** with multi-container setup
- ✅ **API Documentation** (Swagger/ReDoc)
- ✅ **Responsive Frontend** - Clean black, grey, white design

### Bonus Features
- 💳 **Stripe Payment Integration** (test mode)
- 📁 **S3/MinIO File Uploads** for images
- 🔒 **CORS & Security** configured
- 📊 **Admin Panel** with custom models

## 📋 Tech Stack

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS3 (Custom)

### Backend
- **Framework**: Django 4.2 + Django REST Framework 3.14
- **Database**: PostgreSQL 15
- **Authentication**: OAuth (social-auth-app-django) + JWT (simplejwt)
- **Container**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Payment**: Stripe (Bonus)
- **Storage**: AWS S3 / MinIO (Bonus)

## 🏗️ Project Structure

```
ahoum/
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── context/           # Auth context
│   │   ├── services/          # API services
│   │   ├── App.js             # Main app component
│   │   └── index.js           # Entry point
│   ├── public/                # Static files
│   ├── Dockerfile             # Frontend container
│   └── package.json           # Dependencies
├── backend/                    # Django app
│   ├── models.py              # User, Session, Booking models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API views and viewsets
│   ├── authentication.py      # OAuth providers
│   ├── permissions.py         # Custom permissions
│   ├── payment.py             # Stripe integration
│   ├── storage.py             # S3/MinIO file uploads
│   ├── urls.py                # Backend URL routing
│   └── admin.py               # Admin configuration
├── core/                       # Django project
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI configuration
├── nginx/                      # Nginx configuration
│   └── nginx.conf             # Reverse proxy config
├── manage.py                   # Django management
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend Docker image
├── docker-compose.yml          # Multi-container setup
├── docker-entrypoint.sh        # Container startup script
├── .env.example               # Environment variables template
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)
- Google/GitHub OAuth credentials

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ahoum
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Start all services**
```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost/
- **API**: http://localhost/api/
- **Admin**: http://localhost/admin/
- **Swagger**: http://localhost/swagger/
- **ReDoc**: http://localhost/redoc/

4. **Access admin panel**
- Username: `admin`
- Password: `admin123`

### Important Notes

- The frontend runs on port 3000 inside its container
- The backend runs on port 8000 inside its container
- Nginx (port 80) acts as reverse proxy routing:
  - `/` → Frontend
  - `/api/` → Backend API
  - `/admin/` → Django Admin
  - `/swagger/`, `/redoc/` → API Documentation

### Option 2: Local Development

1. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Start PostgreSQL** (make sure it's running)

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

## 🔐 OAuth Setup Instructions

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure consent screen
6. Add authorized redirect URIs:
   - `http://localhost:3000/auth/callback` (frontend)
   - `http://localhost/auth/callback`
7. Copy Client ID and Client Secret to `.env`:
   ```
   GOOGLE_OAUTH_CLIENT_ID=your-client-id
   GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
   ```

### GitHub OAuth Setup

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in application details:
   - Application name: Sessions Marketplace
   - Homepage URL: `http://localhost`
   - Authorization callback URL: `http://localhost:3000/auth/callback`
4. Copy Client ID and Client Secret to `.env`:
   ```
   GITHUB_OAUTH_CLIENT_ID=your-client-id
   GITHUB_OAUTH_CLIENT_SECRET=your-client-secret
   ```

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/oauth/login/        # OAuth login (Google/GitHub)
POST   /api/auth/logout/             # Logout
POST   /api/auth/token/refresh/      # Refresh JWT token
```

### Users
```
GET    /api/users/                   # List users
GET    /api/users/me/                # Current user profile
PUT    /api/users/update_profile/   # Update profile
```

### Sessions
```
GET    /api/sessions/                # List all published sessions (public)
POST   /api/sessions/                # Create session (creator only)
GET    /api/sessions/{id}/           # Session detail
PUT    /api/sessions/{id}/           # Update session (owner only)
DELETE /api/sessions/{id}/           # Delete session (owner only)
GET    /api/sessions/my_sessions/    # Creator's sessions
GET    /api/sessions/{id}/bookings/  # Session bookings (creator only)
```

### Bookings
```
GET    /api/bookings/                # List bookings
POST   /api/bookings/                # Create booking
GET    /api/bookings/{id}/           # Booking detail
PUT    /api/bookings/{id}/           # Update booking
GET    /api/bookings/my_bookings/    # User's bookings
GET    /api/bookings/active/         # Active bookings
GET    /api/bookings/past/           # Past bookings
POST   /api/bookings/{id}/confirm/   # Confirm booking (creator)
POST   /api/bookings/{id}/cancel/    # Cancel booking
```

### Dashboards
```
GET    /api/dashboard/user/          # User dashboard
GET    /api/dashboard/creator/       # Creator dashboard
```

### Payment (Bonus)
```
POST   /api/payment/create-intent/   # Create Stripe payment intent
POST   /api/payment/confirm/         # Confirm payment
POST   /api/payment/webhook/         # Stripe webhook
```

### Storage (Bonus)
```
POST   /api/storage/upload/          # Upload file to S3/MinIO
DELETE /api/storage/delete/          # Delete file
```

## 🎮 Demo Flow

### 1. Login as User
```bash
# Frontend makes OAuth request
POST http://localhost/api/auth/oauth/login/
{
  "provider": "google",
  "access_token": "<google-access-token>",
  "role": "user"
}

# Response
{
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    ...
  },
  "is_new_user": true
}
```

### 2. Browse Sessions (Public)
```bash
GET http://localhost/api/sessions/
```

### 3. Book a Session
```bash
POST http://localhost/api/bookings/
Authorization: Bearer <access-token>
{
  "session": 1,
  "booking_date": "2025-01-15T10:00:00Z",
  "attendees_count": 2,
  "user_notes": "Looking forward to this session!"
}
```

### 4. Create Payment Intent (Bonus)
```bash
POST http://localhost/api/payment/create-intent/
Authorization: Bearer <access-token>
{
  "booking_id": 1
}

# Response
{
  "client_secret": "pi_xxx_secret_yyy",
  "payment_intent_id": "pi_xxx"
}
```

### 5. Login as Creator
```bash
POST http://localhost/api/auth/oauth/login/
{
  "provider": "github",
  "access_token": "<github-access-token>",
  "role": "creator"
}
```

### 6. Create Session
```bash
POST http://localhost/api/sessions/
Authorization: Bearer <access-token>
{
  "title": "Python Web Development Basics",
  "description": "Learn Django and REST Framework",
  "category": "Programming",
  "duration_minutes": 60,
  "price": "49.99",
  "currency": "USD",
  "max_attendees": 10,
  "location": "Online",
  "session_type": "online",
  "status": "published"
}
```

### 7. View Creator Dashboard
```bash
GET http://localhost/api/dashboard/creator/
Authorization: Bearer <access-token>
```

### 8. Manage Bookings
```bash
# Confirm a booking
POST http://localhost/api/bookings/{id}/confirm/
Authorization: Bearer <access-token>
```

## 🐳 Docker Commands

```bash
# Build and start all containers
docker-compose up --build

# Start in detached mode
docker-compose up -d

# Stop all containers
docker-compose down

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access backend shell
docker-compose exec backend python manage.py shell

# Rebuild specific service
docker-compose up --build backend
```

## 🔧 Common Commands

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Start shell
python manage.py shell
```

## 📊 Database Models

### User Model
- Custom user with OAuth support
- Roles: `user`, `creator`
- Fields: username, email, role, avatar, bio, phone, oauth_provider, oauth_id

### Session Model
- Created by creators
- Fields: title, description, category, duration, price, max_attendees, location, type, status
- Status: `draft`, `published`, `cancelled`

### Booking Model
- Created by users
- Fields: user, session, booking_date, attendees_count, total_price, status, payment_status
- Status: `pending`, `confirmed`, `completed`, `cancelled`
- Payment Status: `pending`, `paid`, `failed`, `refunded`

## 🔒 Security Features

- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Custom permissions for endpoints
- CORS configuration
- SQL injection protection (Django ORM)
- XSS protection
- CSRF protection
- Secure password hashing

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test backend

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚢 Production Deployment

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use strong `SECRET_KEY`
4. Configure production database (AWS RDS, etc.)
5. Set up SSL/TLS certificates
6. Use environment variables for secrets
7. Configure Gunicorn workers based on CPU cores
8. Set up monitoring and logging
9. Configure backup strategy
10. Use CDN for static files

## 📝 Environment Variables

See [.env.example](.env.example) for all required environment variables.

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db
```

### Migration Issues
```bash
# Reset migrations
python manage.py migrate backend zero
python manage.py migrate
```

### OAuth Issues
- Verify client IDs and secrets in `.env`
- Check redirect URIs match OAuth app settings
- Ensure access tokens are valid

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Sessions Marketplace Backend Team

## 🙏 Acknowledgments

- Django REST Framework
- PostgreSQL
- Docker
- Stripe
- Social Auth

---

For frontend setup, see the frontend repository README.

