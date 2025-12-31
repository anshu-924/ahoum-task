# 📋 Sessions Marketplace Backend - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Set strong `SECRET_KEY` (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Set `DEBUG=False` for production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up PostgreSQL database credentials
- [ ] Configure CORS origins for your frontend domain

### 2. OAuth Setup
- [ ] Create Google OAuth app
  - [ ] Get Client ID and Secret
  - [ ] Add authorized redirect URIs
  - [ ] Add to `.env`
- [ ] Create GitHub OAuth app
  - [ ] Get Client ID and Secret
  - [ ] Add callback URLs
  - [ ] Add to `.env`

### 3. Database Setup
- [ ] PostgreSQL installed or accessible
- [ ] Database created
- [ ] User created with proper permissions
- [ ] Connection tested

### 4. Optional: Payment Integration
- [ ] Create Stripe account (test mode)
- [ ] Get API keys (publishable and secret)
- [ ] Configure webhook endpoint
- [ ] Add keys to `.env`

### 5. Optional: File Storage
- [ ] Set up AWS S3 or MinIO
- [ ] Create bucket
- [ ] Configure access keys
- [ ] Set CORS policy on bucket
- [ ] Add credentials to `.env`

## 🚀 Deployment Steps

### Docker Deployment (Recommended)

1. **Clone Repository**
   ```bash
   git clone <your-repo-url>
   cd ahoum
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Build and Start**
   ```bash
   docker-compose up --build -d
   ```

4. **Verify Services**
   ```bash
   docker-compose ps
   docker-compose logs backend
   ```

5. **Create Superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Test Endpoints**
   - [ ] API: http://your-domain/api/
   - [ ] Admin: http://your-domain/admin/
   - [ ] Swagger: http://your-domain/swagger/

### Manual Deployment

1. **Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start with Gunicorn**
   ```bash
   gunicorn core.wsgi:application --bind 0.0.0.0:8000
   ```

## 🔒 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` configured
- [ ] HTTPS enabled (SSL/TLS certificate)
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] CORS origins restricted to your frontend domain
- [ ] Database credentials secured
- [ ] OAuth secrets not committed to git
- [ ] Stripe keys using environment variables
- [ ] Admin URL changed (optional)
- [ ] Rate limiting enabled (optional)
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] SQL injection protection (using ORM)
- [ ] XSS protection enabled

## 📊 Post-Deployment Verification

### 1. API Endpoints
- [ ] OAuth login working (Google)
- [ ] OAuth login working (GitHub)
- [ ] JWT token generation working
- [ ] Token refresh working
- [ ] Sessions listing (public)
- [ ] Session creation (creator)
- [ ] Booking creation
- [ ] User dashboard accessible
- [ ] Creator dashboard accessible

### 2. Admin Panel
- [ ] Admin panel accessible
- [ ] Can login with superuser
- [ ] Can view users
- [ ] Can view sessions
- [ ] Can view bookings

### 3. Documentation
- [ ] Swagger UI accessible
- [ ] ReDoc accessible
- [ ] API endpoints documented

### 4. Optional Features
- [ ] Stripe payment working
- [ ] File uploads working
- [ ] Webhooks configured

## 🔍 Testing Checklist

### Functional Testing
- [ ] User can register via OAuth
- [ ] User can login and get JWT tokens
- [ ] User can view profile
- [ ] User can update profile
- [ ] Creator can create sessions
- [ ] User can view sessions catalog
- [ ] User can book a session
- [ ] User can view bookings
- [ ] Creator can view session bookings
- [ ] Creator can confirm bookings
- [ ] User can cancel bookings
- [ ] Payment flow works (if enabled)
- [ ] File upload works (if enabled)

### Security Testing
- [ ] Unauthorized users cannot access protected endpoints
- [ ] Users cannot access creator-only endpoints
- [ ] Users can only see their own bookings
- [ ] Creators can only edit their own sessions
- [ ] CORS properly restricts origins
- [ ] JWT expiration works correctly

### Performance Testing
- [ ] API response times acceptable
- [ ] Database queries optimized
- [ ] Static files served correctly
- [ ] File uploads handle large files

## 📝 Documentation Checklist

- [ ] README.md updated with deployment URL
- [ ] API documentation complete
- [ ] OAuth setup instructions clear
- [ ] Environment variables documented
- [ ] Troubleshooting guide updated
- [ ] Postman collection updated

## 🔄 Continuous Integration

- [ ] GitHub Actions workflow configured
- [ ] Tests run on push
- [ ] Tests run on pull requests
- [ ] Docker build tested
- [ ] Code style checks enabled

## 📈 Monitoring & Maintenance

### Setup Monitoring
- [ ] Error tracking (Sentry, etc.)
- [ ] Application monitoring (New Relic, DataDog, etc.)
- [ ] Log aggregation (CloudWatch, ELK, etc.)
- [ ] Uptime monitoring (UptimeRobot, Pingdom, etc.)
- [ ] Performance monitoring

### Backup Strategy
- [ ] Database backups configured
- [ ] Backup frequency determined
- [ ] Backup retention policy set
- [ ] Restore procedure tested
- [ ] Media files backed up (if applicable)

### Maintenance Tasks
- [ ] Regular dependency updates
- [ ] Security patches applied
- [ ] Database optimization scheduled
- [ ] Log rotation configured
- [ ] Disk space monitoring

## 🎯 Production Optimization

### Performance
- [ ] Database indexes added
- [ ] Query optimization done
- [ ] Caching configured (Redis, Memcached)
- [ ] CDN for static files (CloudFront, etc.)
- [ ] Gzip compression enabled
- [ ] Image optimization

### Scaling
- [ ] Horizontal scaling plan
- [ ] Load balancer configured (if needed)
- [ ] Database connection pooling
- [ ] Background task queue (Celery)
- [ ] Auto-scaling rules (if cloud)

## 📞 Support & Operations

- [ ] Support contact configured
- [ ] Incident response plan
- [ ] Rollback procedure documented
- [ ] On-call rotation (if applicable)
- [ ] Status page setup

## ✅ Final Checklist

Before going live:
- [ ] All environment variables set
- [ ] All tests passing
- [ ] Security audit completed
- [ ] Performance tested
- [ ] Documentation complete
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Team trained
- [ ] Rollback plan ready
- [ ] Go-live date scheduled

## 🎉 Post-Launch

After deployment:
- [ ] Smoke tests passed
- [ ] Monitor error rates
- [ ] Check response times
- [ ] Verify backup jobs
- [ ] Monitor resource usage
- [ ] Gather user feedback
- [ ] Plan first iteration

---

**Note:** This checklist is comprehensive. Not all items may apply to your specific deployment. Adjust as needed based on your requirements and infrastructure.
