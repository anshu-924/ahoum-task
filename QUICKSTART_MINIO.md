# Quick Start: MinIO Image Upload

## ✅ What's Done

### Backend Setup
1. ✅ MinIO container added to docker-compose.yml
2. ✅ Auto-bucket creation (`sessions`) configured
3. ✅ Upload endpoint with automatic thumbnail generation
4. ✅ Image validation (10MB max, image formats only)
5. ✅ Storage service updated with thumbnail support

### Frontend Setup
1. ✅ File upload added to CreateSession form
2. ✅ Image preview functionality
3. ✅ Upload API integration
4. ✅ Styling for file upload component

## 🚀 How to Run

```bash
# Start all services
docker compose up --build
```

This starts:
- MinIO (API: port 9000, Console: port 9001)
- PostgreSQL (port 5432)
- Django Backend (port 8000)
- React Frontend (port 3000)
- Nginx (port 80)

## 🔑 Default Credentials

### MinIO
- **Access Key**: `minioadmin`
- **Secret Key**: `minioadmin123`
- **Bucket**: `sessions` (auto-created with public read)
- **Console URL**: http://localhost:9001

### PostgreSQL
- **User**: `postgres`
- **Password**: `postgres`
- **Database**: `sessions_marketplace`

## 📝 Environment Variables (Already Set)

Your `.env` should have:
```env
USE_S3=True
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin123
AWS_STORAGE_BUCKET_NAME=sessions
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_S3_REGION_NAME=us-east-1
```

## 🎯 How It Works

### 1. User uploads image in CreateSession form
```
User selects image → Preview shown → Form submitted
```

### 2. Backend processes the upload
```javascript
// Frontend sends file
uploadFile(file, 'sessions')
  ↓
// Backend receives and processes
- Validates file (type, size)
- Generates unique filename
- Uploads original to MinIO: sessions/abc123.jpg
- Creates thumbnail (300x300px)
- Uploads thumbnail: sessions/thumbnails/abc123_thumb.jpg
- Returns both URLs
```

### 3. Session created with URLs
```json
{
  "title": "My Session",
  "image_url": "http://localhost:9000/sessions/sessions/abc123.jpg",
  "thumbnail_url": "http://localhost:9000/sessions/sessions/thumbnails/abc123_thumb.jpg",
  ...
}
```

## 📁 File Structure

```
sessions/
├── abc123.jpg              ← Original image
├── def456.jpg
├── thumbnails/
│   ├── abc123_thumb.jpg    ← Auto-generated thumbnail
│   └── def456_thumb.jpg
```

## 🔍 Verify Setup

1. **Check MinIO Console**
   - Go to http://localhost:9001
   - Login: minioadmin / minioadmin123
   - Verify `sessions` bucket exists

2. **Test Upload**
   - Create a session with an image
   - Check MinIO console for uploaded files
   - Verify thumbnail was created

3. **Check URLs**
   - Image URLs should be accessible
   - Format: `http://localhost:9000/sessions/sessions/[filename].jpg`

## 📦 API Endpoints

### Upload File
```
POST /api/storage/upload/
Content-Type: multipart/form-data
Authorization: Bearer <token>

Body:
- file: [image file]
- folder: "sessions" (optional)

Response:
{
  "image_url": "http://localhost:9000/sessions/sessions/abc123.jpg",
  "thumbnail_url": "http://localhost:9000/sessions/sessions/thumbnails/abc123_thumb.jpg",
  "filename": "abc123.jpg",
  "key": "sessions/abc123.jpg"
}
```

### Delete File
```
DELETE /api/storage/delete/
Content-Type: application/json
Authorization: Bearer <token>

Body:
{
  "key": "sessions/abc123.jpg"
}
```

## 🎨 Frontend Integration

The CreateSession form now includes:
- File input with drag-and-drop styling
- Image preview before upload
- Remove button for selected image
- Upload progress indication
- Automatic URL population

## 🐛 Troubleshooting

### MinIO not accessible
```bash
# Check container status
docker ps | grep minio

# Check MinIO logs
docker logs sessions_minio

# Test MinIO health
curl http://localhost:9000/minio/health/live
```

### Bucket not created
```bash
# Recreate bucket manually
docker exec sessions_minio_setup /bin/sh -c "
/usr/bin/mc alias set myminio http://minio:9000 minioadmin minioadmin123
/usr/bin/mc mb myminio/sessions --ignore-existing
/usr/bin/mc anonymous set public myminio/sessions
"
```

### Upload fails
- Check USE_S3=True in .env
- Verify MinIO container is running
- Check file size (< 10MB)
- Verify file is an image format

### Images not displaying
- URLs use `localhost:9000` for external access
- Inside Docker, services use `minio:9000`
- Check bucket policy is set to public

## 📚 Next Steps

1. **Update EditSession** - Add same upload functionality
2. **Display thumbnails** - Show in session cards and listings
3. **Add image cropping** - Allow users to crop before upload
4. **Implement CDN** - For production, use CloudFront or similar
5. **Add delete feature** - Delete old images when updating

## 📖 Full Documentation

See [MINIO_SETUP.md](./MINIO_SETUP.md) for detailed documentation.
