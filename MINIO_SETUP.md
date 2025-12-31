# MinIO Setup Guide

## Overview
This project uses MinIO as an S3-compatible object storage for storing session thumbnail images.

## Default Credentials
- **Access Key**: `minioadmin`
- **Secret Key**: `minioadmin123`
- **Bucket Name**: `sessions`

## Services & Ports
- **MinIO API**: http://localhost:9000
- **MinIO Console (Web UI)**: http://localhost:9001

## Getting Started

### 1. Start the Services
```bash
docker compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- MinIO object storage (ports 9000, 9001)
- Django backend (port 8000)
- React frontend (port 3000)
- Nginx reverse proxy (port 80)

### 2. Access MinIO Console
Open your browser and go to: http://localhost:9001

Login with:
- Username: `minioadmin`
- Password: `minioadmin123`

You'll see the `sessions` bucket already created with public read access.

## Using the File Upload API

### Upload a Session Thumbnail

**Endpoint**: `POST /api/storage/upload/`

**Headers**:
```
Authorization: Bearer <your-jwt-token>
Content-Type: multipart/form-data
```

**Body** (form-data):
- `file`: The image file to upload
- `folder`: (optional) Folder name, defaults to "sessions"

**Example using curl**:
```bash
curl -X POST http://localhost:8000/api/storage/upload/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "folder=sessions"
```

**Response**:
```json
{
  "image_url": "http://localhost:9000/sessions/sessions/abc123.jpg",
  "thumbnail_url": "http://localhost:9000/sessions/sessions/thumbnails/abc123_thumb.jpg",
  "filename": "abc123.jpg",
  "key": "sessions/abc123.jpg"
}
```

### Create/Update Session with Thumbnail

After uploading the image, use the returned URLs to create or update a session:

**Endpoint**: `POST /api/sessions/`

```json
{
  "title": "1-on-1 Coaching Session",
  "description": "Personal coaching session",
  "category": "Coaching",
  "duration_minutes": 60,
  "price": "99.99",
  "image_url": "http://localhost:9000/sessions/sessions/abc123.jpg",
  "thumbnail_url": "http://localhost:9000/sessions/sessions/thumbnails/abc123_thumb.jpg",
  "status": "published"
}
```

## Features

### Automatic Thumbnail Generation
When you upload an image:
1. The original image is stored in `sessions/` folder
2. A thumbnail (max 300x300px) is automatically generated and stored in `sessions/thumbnails/`
3. Both URLs are returned in the response

### File Validation
- **Max file size**: 10MB
- **Allowed types**: JPEG, JPG, PNG, GIF, WebP
- **Format**: Thumbnails are converted to JPEG for optimal size

## Frontend Integration

### Example React Code

```javascript
import api from './services/api';

const uploadThumbnail = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('folder', 'sessions');
  
  try {
    const response = await api.post('/storage/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
    // Returns: { image_url, thumbnail_url, filename, key }
  } catch (error) {
    console.error('Upload failed:', error);
    throw error;
  }
};

// Usage in session creation
const createSession = async (sessionData, thumbnailFile) => {
  // 1. Upload thumbnail first
  const uploadResult = await uploadThumbnail(thumbnailFile);
  
  // 2. Create session with uploaded URLs
  const session = await api.post('/sessions/', {
    ...sessionData,
    image_url: uploadResult.image_url,
    thumbnail_url: uploadResult.thumbnail_url
  });
  
  return session.data;
};
```

## Environment Variables

Make sure your `.env` file has these settings:

```env
USE_S3=True
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin123
AWS_STORAGE_BUCKET_NAME=sessions
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_S3_REGION_NAME=us-east-1
```

## Troubleshooting

### Cannot connect to MinIO
- Ensure MinIO container is running: `docker ps | grep minio`
- Check MinIO health: `curl http://localhost:9000/minio/health/live`

### Upload fails with 403 Forbidden
- Verify the bucket policy is set to public-read
- Check MinIO console at http://localhost:9001
- Go to Buckets → sessions → Access Policy → Set to "Public"

### Images not displaying
- For external access, MinIO URLs use `localhost:9000`
- Inside Docker network, services use `minio:9000`
- The backend automatically converts URLs for external access

### Delete a file

**Endpoint**: `DELETE /api/storage/delete/`

```bash
curl -X DELETE http://localhost:8000/api/storage/delete/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "sessions/abc123.jpg"}'
```

## Production Considerations

For production, you should:
1. Change MinIO credentials (use strong passwords)
2. Use HTTPS for MinIO endpoint
3. Set up proper bucket policies
4. Configure CDN for faster image delivery
5. Use AWS S3 instead of MinIO for better scalability
6. Set up backup and replication policies

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│    Backend   │─────▶│    MinIO    │
│   (React)   │      │   (Django)   │      │  (Storage)  │
└─────────────┘      └──────────────┘      └─────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │  PostgreSQL  │
                     │  (Database)  │
                     └──────────────┘
```

## Next Steps

1. Update your frontend to include file upload functionality
2. Add drag-and-drop image upload to session creation form
3. Display thumbnails in session listings
4. Add image cropping/editing features
5. Implement image optimization and compression
