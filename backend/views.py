from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.utils import timezone
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.views.decorators.cache import cache_page
import requests
from .models import Session, Booking
from .serializers import (
    UserSerializer, UserProfileUpdateSerializer,
    SessionListSerializer, SessionDetailSerializer, SessionCreateUpdateSerializer,
    BookingListSerializer, BookingDetailSerializer, BookingCreateSerializer,
    BookingUpdateSerializer, OAuthLoginSerializer
)
from .authentication import OAuthProvider, get_tokens_for_user
from .permissions import IsCreator, IsOwnerOrReadOnly, IsBookingOwnerOrSessionCreator

User = get_user_model()


# Custom throttle classes
class AuthRateThrottle(UserRateThrottle):
    rate = '10/minute'


class BookingCreateThrottle(UserRateThrottle):
    rate = '20/hour'


class SessionCreateThrottle(UserRateThrottle):
    rate = '10/hour'


class PaymentThrottle(UserRateThrottle):
    rate = '10/hour'


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def oauth_login(request):
    """
    OAuth login endpoint
    Accepts provider (google/github) and access_token
    Returns JWT tokens and user info
    Rate limited to 10 requests per minute per IP
    """
    serializer = OAuthLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    provider_name = serializer.validated_data['provider']
    access_token = serializer.validated_data['access_token']
    role = serializer.validated_data.get('role', 'user')
    
    # Get the appropriate OAuth provider
    provider_class = OAuthProvider.get_provider(provider_name)
    if not provider_class:
        return Response(
            {'error': 'Invalid OAuth provider'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get user info from OAuth provider
        user_info = provider_class.get_user_info(access_token)
        
        # Create or update user
        user, created = provider_class.create_or_update_user(user_info)
        
        # Set role if new user
        if created:
            user.role = role
            user.save()
        
        # Generate JWT tokens
        tokens = get_tokens_for_user(user)
        
        return Response({
            'tokens': tokens,
            'user': UserSerializer(user).data,
            'is_new_user': created
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def github_code_exchange(request):
    """
    Exchange GitHub authorization code for access token
    Then perform OAuth login
    Rate limited to 10 requests per minute per IP
    """
    code = request.data.get('code')
    role = request.data.get('role', 'user')
    
    if not code:
        return Response(
            {'error': 'Authorization code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Exchange code for access token
        token_url = 'https://github.com/login/oauth/access_token'
        token_data = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code
        }
        headers = {'Accept': 'application/json'}
        
        token_response = requests.post(token_url, data=token_data, headers=headers)
        token_json = token_response.json()
        
        if 'error' in token_json:
            return Response(
                {'error': token_json.get('error_description', 'Failed to exchange code')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        access_token = token_json.get('access_token')
        
        if not access_token:
            return Response(
                {'error': 'No access token received from GitHub'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Now use the access token to log in
        provider_class = OAuthProvider.get_provider('github')
        user_info = provider_class.get_user_info(access_token)
        user, created = provider_class.create_or_update_user(user_info)
        
        if created:
            user.role = role
            user.save()
        
        tokens = get_tokens_for_user(user)
        
        return Response({
            'tokens': tokens,
            'user': UserSerializer(user).data,
            'is_new_user': created
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout endpoint (client should discard tokens)"""
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User operations
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.all()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)


class SessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Session CRUD operations
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SessionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SessionCreateUpdateSerializer
        return SessionDetailSerializer
    
    def get_queryset(self):
        queryset = Session.objects.select_related('creator').annotate(
            bookings_count=Count('bookings')
        )
        
        # Public catalog: only published sessions
        if self.action == 'list':
            queryset = queryset.filter(status='published')
        
        # Creator can see their own sessions
        if self.request.user.is_authenticated and hasattr(self.request.user, 'role'):
            if self.request.user.role == 'creator' and self.action == 'my_sessions':
                queryset = queryset.filter(creator=self.request.user)
        
        return queryset
    
    def get_permissions(self):
        """Allow anyone to list/retrieve sessions, but only creators to create/modify"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create']:
            return [IsAuthenticated(), IsCreator()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()
    
    def get_throttles(self):
        """Apply stricter throttling for session creation"""
        if self.action == 'create':
            return [SessionCreateThrottle()]
        return super().get_throttles()
    
    def get_throttles(self):
        """Apply stricter throttling for session creation"""
        if self.action == 'create':
            return [SessionCreateThrottle()]
        return super().get_throttles()
    
    def perform_create(self, serializer):
        """Set creator to current user"""
        if self.request.user.role != 'creator':
            raise permissions.PermissionDenied("Only creators can create sessions")
        serializer.save(creator=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsCreator])
    def my_sessions(self, request):
        """Get all sessions created by current user"""
        sessions = self.get_queryset().filter(creator=request.user)
        serializer = SessionListSerializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a session (only for session creator)"""
        session = self.get_object()
        if request.user != session.creator:
            return Response(
                {'error': 'You do not have permission to view bookings for this session'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        bookings = session.bookings.select_related('user').all()
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking operations
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        elif self.action == 'create':
            return BookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        return BookingDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.select_related('user', 'session', 'session__creator')
        
        # Users see their own bookings
        if user.role == 'user':
            queryset = queryset.filter(user=user)
        # Creators see bookings for their sessions
        elif user.role == 'creator':
            queryset = queryset.filter(Q(user=user) | Q(session__creator=user))
        
        return queryset
    
    def get_permissions(self):
        """Check permissions based on action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsBookingOwnerOrSessionCreator()]
        return super().get_permissions()
    
    def get_throttles(self):
        """Apply stricter throttling for booking creation"""
        if self.action == 'create':
            return [BookingCreateThrottle()]
        return super().get_throttles()
    
    def get_throttles(self):
        """Apply stricter throttling for booking creation"""
        if self.action == 'create':
            return [BookingCreateThrottle()]
        return super().get_throttles()
    
    def perform_create(self, serializer):
        """Create booking with current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get all bookings for current user"""
        bookings = self.get_queryset().filter(user=request.user)
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active bookings (pending/confirmed)"""
        bookings = self.get_queryset().filter(
            status__in=['pending', 'confirmed']
        )
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get past bookings (completed/cancelled)"""
        bookings = self.get_queryset().filter(
            status__in=['completed', 'cancelled']
        )
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (creator only)"""
        booking = self.get_object()
        if request.user != booking.session.creator:
            return Response(
                {'error': 'Only session creator can confirm bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.status = 'confirmed'
        booking.save()
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # User can cancel their own booking, creator can cancel any booking for their session
        if request.user != booking.user and request.user != booking.session.creator:
            return Response(
                {'error': 'You do not have permission to cancel this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.status = 'cancelled'
        booking.save()
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data)


# Dashboard views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """
    User dashboard with bookings and profile
    """
    user = request.user
    
    # Get user bookings
    active_bookings = Booking.objects.filter(
        user=user,
        status__in=['pending', 'confirmed']
    ).select_related('session', 'session__creator')
    
    past_bookings = Booking.objects.filter(
        user=user,
        status__in=['completed', 'cancelled']
    ).select_related('session', 'session__creator')
    
    return Response({
        'user': UserSerializer(user).data,
        'active_bookings': BookingListSerializer(active_bookings, many=True).data,
        'past_bookings': BookingListSerializer(past_bookings, many=True).data,
        'total_bookings': active_bookings.count() + past_bookings.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCreator])
def creator_dashboard(request):
    """
    Creator dashboard with sessions and bookings overview
    """
    user = request.user
    
    if user.role != 'creator':
        return Response(
            {'error': 'Only creators can access this dashboard'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get creator's sessions
    sessions = Session.objects.filter(creator=user).annotate(
        bookings_count=Count('bookings')
    )
    
    # Get bookings for creator's sessions
    all_bookings = Booking.objects.filter(
        session__creator=user
    ).select_related('user', 'session')
    
    pending_bookings = all_bookings.filter(status='pending')
    confirmed_bookings = all_bookings.filter(status='confirmed')
    
    return Response({
        'user': UserSerializer(user).data,
        'sessions': SessionListSerializer(sessions, many=True).data,
        'pending_bookings': BookingListSerializer(pending_bookings, many=True).data,
        'confirmed_bookings': BookingListSerializer(confirmed_bookings, many=True).data,
        'stats': {
            'total_sessions': sessions.count(),
            'published_sessions': sessions.filter(status='published').count(),
            'total_bookings': all_bookings.count(),
            'pending_bookings': pending_bookings.count(),
            'confirmed_bookings': confirmed_bookings.count(),
        }
    })

