# MinIO Setup Summary

## ✅ Everything is Ready to Run!

I've configured MinIO/S3 storage for your session marketplace application. Here's what was done:

## 🎯 Changes Made

### 1. Docker Configuration
- **Added MinIO service** to [docker-compose.yml](docker-compose.yml)
  - API on port 9000
  - Web Console on port 9001
  - Automatic bucket creation (`sessions`)
  - Public read access configured

### 2. Backend Updates
- **Updated** [backend/storage.py](backend/storage.py)
  - Added automatic thumbnail generation (300x300px)
  - Image validation (10MB max, images only)
  - Returns both `image_url` and `thumbnail_url`
  - Proper error handling

### 3. Frontend Updates
- **Updated** [frontend/src/pages/CreateSession.js](frontend/src/pages/CreateSession.js)
  - Added file upload input
  - Image preview before upload
  - Progress indicators
  
- **Updated** [frontend/src/services/api.js](frontend/src/services/api.js)
  - Added `uploadFile()` function
  - Added `deleteFile()` function
  
- **Updated** [frontend/src/pages/CreateSession.css](frontend/src/pages/CreateSession.css)
  - Styled file input
  - Thumbnail preview styles

### 4. Configuration
- **Updated** [.env.example](.env.example)
  - MinIO credentials documented
  - Default values provided

## 🔑 Default Credentials (Already Set)

### MinIO
```
Access Key: minioadmin
Secret Key: minioadmin123
Bucket: sessions (auto-created)
Console: http://localhost:9001
API: http://localhost:9000
```

### No Additional Configuration Needed!
All credentials are already configured in docker-compose.yml with default values.

## 🚀 How to Start

Just run:
```bash
docker compose up --build
```

That's it! The system will:
1. Start PostgreSQL database
2. Start MinIO object storage
3. Create `sessions` bucket automatically
4. Set bucket to public read
5. Start Django backend with MinIO configured
6. Start React frontend
7. Start Nginx reverse proxy

## 📖 How to Use

### From the UI (Easiest)
1. Navigate to Create Session page
2. Fill out the form
3. Click "Choose File" to select an image
4. See preview of your image
5. Submit the form
6. Image is automatically uploaded and URLs are saved

### What Happens Behind the Scenes
```
User selects image
   ↓
Preview shown
   ↓
Form submitted
   ↓
Image uploaded to MinIO
   ↓
Thumbnail auto-generated (300x300px)
   ↓
Both URLs returned
   ↓
Session created with URLs in database
```

## 🔍 Verify It's Working

1. **Check MinIO Console**
   - Visit: http://localhost:9001
   - Login: minioadmin / minioadmin123
   - See the `sessions` bucket

2. **Upload Test**
   - Create a session with an image
   - Check MinIO console for files
   - Verify thumbnail was created in `sessions/thumbnails/`

3. **Check URLs**
   - Original: `http://localhost:9000/sessions/sessions/[uuid].jpg`
   - Thumbnail: `http://localhost:9000/sessions/sessions/thumbnails/[uuid]_thumb.jpg`

## 📁 File Organization

MinIO stores files like this:
```
sessions/                          ← Bucket name
├── sessions/                      ← Folder for originals
│   ├── abc-123-def.jpg           ← Original images
│   ├── xyz-789-ghi.png
│   └── thumbnails/               ← Subfolder for thumbnails
│       ├── abc-123-def_thumb.jpg ← Auto-generated 300x300
│       └── xyz-789-ghi_thumb.png
```

## 🎨 Model Fields

Your Session model already has:
- `image_url` - Stores original image URL
- `thumbnail_url` - Stores thumbnail URL

Both are populated automatically when you upload!

## 🐛 Quick Troubleshooting

### Problem: MinIO container won't start
```bash
docker ps -a | grep minio  # Check status
docker logs sessions_minio  # Check logs
```

### Problem: Bucket not created
```bash
docker exec sessions_minio_setup /bin/sh -c "
/usr/bin/mc alias set myminio http://minio:9000 minioadmin minioadmin123
/usr/bin/mc mb myminio/sessions --ignore-existing
/usr/bin/mc anonymous set public myminio/sessions
"
```

### Problem: Upload fails with 400/500
- Check `USE_S3=True` in your .env file
- Verify MinIO is running: `docker ps | grep minio`
- Check file size (must be < 10MB)
- Check file type (must be image)

## 📚 Documentation

Full documentation available in:
- **[MINIO_SETUP.md](MINIO_SETUP.md)** - Detailed setup and API usage
- **[QUICKSTART_MINIO.md](QUICKSTART_MINIO.md)** - Quick reference guide

## 🎉 Ready to Go!

Everything is configured with sensible defaults. Just run `docker compose up --build` and you're ready to upload images!

No additional setup or configuration required. All credentials are using default values as requested.
