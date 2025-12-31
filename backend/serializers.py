from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Session, Booking

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                  'avatar', 'bio', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at', 'username']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'phone']


class SessionListSerializer(serializers.ModelSerializer):
    """Serializer for listing sessions (catalog)"""
    creator_name = serializers.CharField(source='creator.get_full_name', read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    bookings_count = serializers.IntegerField(source='bookings.count', read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'title', 'description', 'category', 'duration_minutes', 
                  'price', 'currency', 'max_attendees', 'location', 'session_type',
                  'image_url', 'thumbnail_url', 'status', 'creator_name', 
                  'creator_username', 'bookings_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class SessionDetailSerializer(serializers.ModelSerializer):
    """Serializer for session detail view"""
    creator = UserSerializer(read_only=True)
    bookings_count = serializers.IntegerField(source='bookings.count', read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'creator', 'title', 'description', 'category', 
                  'duration_minutes', 'price', 'currency', 'max_attendees', 
                  'location', 'session_type', 'image_url', 'thumbnail_url', 
                  'status', 'is_available', 'bookings_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SessionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating sessions"""
    
    class Meta:
        model = Session
        fields = ['title', 'description', 'category', 'duration_minutes', 'price', 
                  'currency', 'max_attendees', 'location', 'session_type', 
                  'image_url', 'thumbnail_url', 'status']
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be non-negative")
        return value
    
    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return value


class BookingListSerializer(serializers.ModelSerializer):
    """Serializer for listing bookings"""
    session_title = serializers.CharField(source='session.title', read_only=True)
    session_image = serializers.URLField(source='session.thumbnail_url', read_only=True)
    creator_name = serializers.CharField(source='session.creator.get_full_name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'session', 'session_title', 'session_image', 'creator_name',
                  'user_name', 'booking_date', 'attendees_count', 'total_price', 
                  'status', 'payment_status', 'is_active', 'is_past', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookingDetailSerializer(serializers.ModelSerializer):
    """Serializer for booking detail view"""
    session = SessionDetailSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'session', 'booking_date', 'attendees_count', 
                  'total_price', 'status', 'payment_status', 'payment_intent_id',
                  'payment_method', 'user_notes', 'creator_notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    
    class Meta:
        model = Booking
        fields = ['session', 'booking_date', 'attendees_count', 'user_notes']
    
    def validate(self, data):
        session = data.get('session')
        attendees_count = data.get('attendees_count', 1)
        
        # Check if session is available
        if not session.is_available:
            raise serializers.ValidationError("This session is not available for booking")
        
        # Check attendees count
        if attendees_count > session.max_attendees:
            raise serializers.ValidationError(
                f"Maximum {session.max_attendees} attendees allowed for this session"
            )
        
        return data
    
    def create(self, validated_data):
        session = validated_data['session']
        attendees_count = validated_data.get('attendees_count', 1)
        
        # Calculate total price
        total_price = session.price * attendees_count
        
        # Create booking with the user from request context
        booking = Booking.objects.create(
            user=self.context['request'].user,
            session=session,
            booking_date=validated_data['booking_date'],
            attendees_count=attendees_count,
            user_notes=validated_data.get('user_notes', ''),
            total_price=total_price,
            status='pending',
            payment_status='pending'
        )
        
        return booking


class BookingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating booking status"""
    
    class Meta:
        model = Booking
        fields = ['status', 'payment_status', 'creator_notes']


class OAuthLoginSerializer(serializers.Serializer):
    """Serializer for OAuth login"""
    provider = serializers.ChoiceField(choices=['google', 'github'])
    access_token = serializers.CharField()
    role = serializers.ChoiceField(choices=['user', 'creator'], required=False, default='user')

