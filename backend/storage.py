import boto3
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from botocore.exceptions import ClientError
from PIL import Image
import io
import uuid
import os


def get_s3_client():
    """Get S3/MinIO client"""
    return boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL if settings.USE_S3 else None,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID if settings.USE_S3 else None,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY if settings.USE_S3 else None,
        region_name=settings.AWS_S3_REGION_NAME if settings.USE_S3 else None,
    )


def create_thumbnail(image_file, max_size=(300, 300)):
    """Create a thumbnail from an image file"""
    try:
        image = Image.open(image_file)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            image = rgb_image
        
        # Save to bytes
        thumb_io = io.BytesIO()
        image.save(thumb_io, format='JPEG', quality=85, optimize=True)
        thumb_io.seek(0)
        return thumb_io
    except Exception as e:
        raise Exception(f"Failed to create thumbnail: {str(e)}")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    """
    Upload file to S3/MinIO with automatic thumbnail generation for images
    Returns both image_url and thumbnail_url
    """
    if not settings.USE_S3:
        return Response(
            {'error': 'File storage is not configured'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file_obj = request.FILES.get('file')
    if not file_obj:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file size (max 10MB)
    if file_obj.size > 10 * 1024 * 1024:
        return Response(
            {'error': 'File size exceeds 10MB limit'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file type (images only for now)
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if file_obj.content_type not in allowed_types:
        return Response(
            {'error': 'Invalid file type. Only images are allowed'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Generate unique filename
        ext = os.path.splitext(file_obj.name)[1]
        base_filename = str(uuid.uuid4())
        original_filename = f"{base_filename}{ext}"
        thumbnail_filename = f"{base_filename}_thumb{ext}"
        
        folder = request.data.get('folder', 'sessions')
        original_key = f"{folder}/{original_filename}"
        thumbnail_key = f"{folder}/thumbnails/{thumbnail_filename}"
        
        s3_client = get_s3_client()
        
        # Upload original image
        file_obj.seek(0)
        s3_client.upload_fileobj(
            file_obj,
            settings.AWS_STORAGE_BUCKET_NAME,
            original_key,
            ExtraArgs={
                'ContentType': file_obj.content_type,
                'ACL': 'public-read'
            }
        )
        
        # Create and upload thumbnail
        file_obj.seek(0)
        thumbnail_io = create_thumbnail(file_obj)
        s3_client.upload_fileobj(
            thumbnail_io,
            settings.AWS_STORAGE_BUCKET_NAME,
            thumbnail_key,
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'ACL': 'public-read'
            }
        )
        
        # Generate URLs
        if settings.AWS_S3_CUSTOM_DOMAIN:
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{original_key}"
            thumbnail_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{thumbnail_key}"
        else:
            # For MinIO in Docker, use localhost:9000 for external access
            endpoint = settings.AWS_S3_ENDPOINT_URL.replace('minio', 'localhost')
            image_url = f"{endpoint}/{settings.AWS_STORAGE_BUCKET_NAME}/{original_key}"
            thumbnail_url = f"{endpoint}/{settings.AWS_STORAGE_BUCKET_NAME}/{thumbnail_key}"
        
        return Response({
            'image_url': image_url,
            'thumbnail_url': thumbnail_url,
            'filename': original_filename,
            'key': original_key,
        })
    
    except Exception as e:
        return Response(
            {'error': f'Upload failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request):
    """
    Delete file from S3/MinIO
    """
    if not settings.USE_S3:
        return Response(
            {'error': 'File storage is not configured'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    key = request.data.get('key')
    if not key:
        return Response(
            {'error': 'File key is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        s3_client = get_s3_client()
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key
        )
        
        return Response({
            'message': 'File deleted successfully'
        })
    
    except ClientError as e:
        return Response(
            {'error': f'Delete failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
