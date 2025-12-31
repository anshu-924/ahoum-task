# Troubleshooting Guide

## Common Issues and Solutions

### 1. Database Connection Issues

#### Problem: "could not connect to server"
```
django.db.utils.OperationalError: could not connect to server: Connection refused
```

**Solutions:**
- Check if PostgreSQL is running:
  ```bash
  # Docker
  docker-compose ps
  
  # Local
  # Windows
  Get-Service postgresql*
  
  # Linux/Mac
  sudo systemctl status postgresql
  ```

- Verify database credentials in `.env`:
  ```env
  DB_HOST=localhost  # or 'db' for Docker
  DB_PORT=5432
  DB_NAME=sessions_marketplace
  DB_USER=postgres
  DB_PASSWORD=postgres
  ```

- Wait for database to be ready (Docker):
  ```bash
  docker-compose logs db
  ```

### 2. Migration Issues

#### Problem: "No migrations to apply"
**Solution:**
```bash
python manage.py makemigrations backend
python manage.py migrate
```

#### Problem: "Migration is already applied"
**Solution:**
```bash
# Reset migrations
python manage.py migrate backend zero
python manage.py migrate
```

#### Problem: "Table already exists"
**Solution:**
```bash
# Fake initial migration
python manage.py migrate --fake-initial
```

### 3. OAuth Authentication Issues

#### Problem: "Invalid OAuth provider"
**Solution:**
- Verify OAuth credentials in `.env`:
  ```env
  GOOGLE_OAUTH_CLIENT_ID=your-client-id
  GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
  ```

#### Problem: "Failed to fetch user info"
**Solutions:**
- Verify access token is valid and not expired
- Check OAuth app redirect URIs match your frontend URL
- Ensure OAuth scopes include email and profile

#### Problem: "redirect_uri_mismatch"
**Solution:**
- Add authorized redirect URI in OAuth app settings:
  - Google: `http://localhost:3000/auth/callback`
  - GitHub: `http://localhost:3000/auth/callback`

### 4. JWT Token Issues

#### Problem: "Token is invalid or expired"
**Solutions:**
- Use refresh token to get new access token:
  ```bash
  POST /api/auth/token/refresh/
  {
    "refresh": "your-refresh-token"
  }
  ```

- Check token expiration settings in `settings.py`:
  ```python
  SIMPLE_JWT = {
      'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
      'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
  }
  ```

#### Problem: "Authentication credentials were not provided"
**Solution:**
- Include Authorization header:
  ```
  Authorization: Bearer your-access-token
  ```

### 5. Docker Issues

#### Problem: "Port already allocated"
**Solutions:**
```bash
# Check what's using the port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Stop conflicting service or change port in docker-compose.yml
```

#### Problem: "Container exits immediately"
**Solutions:**
```bash
# Check container logs
docker-compose logs backend

# Common issues:
# - Database not ready: Wait or increase sleep time in entrypoint
# - Missing environment variables: Check .env file
# - Migration errors: Check logs for details
```

#### Problem: "Cannot connect to the Docker daemon"
**Solutions:**
- Start Docker Desktop (Windows/Mac)
- Start Docker service (Linux):
  ```bash
  sudo systemctl start docker
  ```

### 6. CORS Issues

#### Problem: "CORS header 'Access-Control-Allow-Origin' missing"
**Solutions:**
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`:
  ```env
  CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
  ```

- Ensure CORS middleware is enabled in `settings.py`:
  ```python
  MIDDLEWARE = [
      ...
      'corsheaders.middleware.CorsMiddleware',
      ...
  ]
  ```

### 7. Static Files Issues

#### Problem: "Static files not loading"
**Solutions:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# For Docker
docker-compose exec backend python manage.py collectstatic --noinput
```

#### Problem: "404 for static files"
**Solution:**
- Check `STATIC_URL` and `STATIC_ROOT` in settings
- Ensure WhiteNoise is configured properly
- Verify Nginx configuration for Docker setup

### 8. Permission Issues

#### Problem: "You do not have permission to perform this action"
**Solutions:**
- Check user role (user vs creator)
- Verify authentication token is valid
- Check endpoint permissions in `views.py`

#### Problem: "Only creators can create sessions"
**Solution:**
- Login with creator role:
  ```json
  {
    "provider": "google",
    "access_token": "...",
    "role": "creator"
  }
  ```

### 9. Payment Integration Issues

#### Problem: "Stripe API key is invalid"
**Solutions:**
- Verify Stripe keys in `.env`:
  ```env
  STRIPE_PUBLISHABLE_KEY=pk_test_...
  STRIPE_SECRET_KEY=sk_test_...
  ```
- Ensure using test keys for development

#### Problem: "Payment intent creation failed"
**Solutions:**
- Check booking exists and belongs to user
- Verify booking is not already paid
- Check Stripe account is active

### 10. File Upload Issues

#### Problem: "File storage is not configured"
**Solution:**
- Enable S3 in `.env`:
  ```env
  USE_S3=True
  AWS_ACCESS_KEY_ID=your-key
  AWS_SECRET_ACCESS_KEY=your-secret
  AWS_STORAGE_BUCKET_NAME=your-bucket
  ```

#### Problem: "File size exceeds limit"
**Solution:**
- File size limit is 10MB by default
- Modify in `backend/storage.py` if needed

#### Problem: "Invalid file type"
**Solution:**
- Only images are allowed by default
- Supported: JPEG, JPG, PNG, GIF, WebP

### 11. Admin Panel Issues

#### Problem: "Cannot access admin panel"
**Solutions:**
```bash
# Create superuser
python manage.py createsuperuser

# For Docker
docker-compose exec backend python manage.py createsuperuser

# Default credentials (Docker)
Username: admin
Password: admin123
```

#### Problem: "CSRF verification failed"
**Solution:**
- Clear browser cookies
- Ensure CSRF middleware is enabled
- Use Django admin login page directly

### 12. Development Server Issues

#### Problem: "Port 8000 is already in use"
**Solutions:**
```bash
# Use different port
python manage.py runserver 8080

# Find and kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

#### Problem: "Server keeps restarting"
**Solutions:**
- Check for syntax errors in Python files
- Verify all dependencies are installed
- Check logs for error messages

### 13. Testing Issues

#### Problem: "Tests fail with database errors"
**Solution:**
- Use separate test database (Django creates automatically)
- Check database permissions
- Ensure PostgreSQL is running

#### Problem: "Import errors in tests"
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Getting Help

If you're still experiencing issues:

1. **Check logs:**
   ```bash
   # Docker
   docker-compose logs -f backend
   
   # Local
   # Logs are printed to console
   ```

2. **Check Django debug page** (if DEBUG=True)

3. **Test with Swagger UI:** http://localhost/swagger/

4. **Use Postman collection** for API testing

5. **Run tests:**
   ```bash
   python manage.py test backend
   ```

6. **Check GitHub Issues** or create a new one

## Useful Commands

```bash
# Docker
docker-compose up --build          # Rebuild and start
docker-compose down -v            # Stop and remove volumes
docker-compose logs -f backend    # Follow logs
docker-compose exec backend bash  # Access container shell

# Django
python manage.py check            # Check for issues
python manage.py shell           # Django shell
python manage.py dbshell         # Database shell
python manage.py showmigrations  # Show migrations status

# Database
python manage.py dumpdata > backup.json  # Backup data
python manage.py loaddata backup.json    # Restore data
```
