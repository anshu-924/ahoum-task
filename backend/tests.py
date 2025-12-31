from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import Session, Booking
from decimal import Decimal
from django.utils import timezone

User = get_user_model()


class AuthenticationTests(TestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='user'
        )
        self.creator = User.objects.create_user(
            username='testcreator',
            email='creator@example.com',
            password='testpass123',
            role='creator'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.role, 'user')
        self.assertEqual(self.creator.role, 'creator')


class SessionTests(TestCase):
    """Test session endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.creator = User.objects.create_user(
            username='creator',
            email='creator@example.com',
            password='testpass123',
            role='creator'
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123',
            role='user'
        )
        self.session = Session.objects.create(
            creator=self.creator,
            title='Test Session',
            description='Test Description',
            category='Programming',
            duration_minutes=60,
            price=Decimal('49.99'),
            currency='USD',
            max_attendees=10,
            session_type='online',
            status='published'
        )
    
    def test_list_sessions(self):
        """Test listing sessions (public)"""
        response = self.client.get('/api/sessions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_session_as_creator(self):
        """Test creating session as creator"""
        self.client.force_authenticate(user=self.creator)
        data = {
            'title': 'New Session',
            'description': 'New Description',
            'category': 'Design',
            'duration_minutes': 90,
            'price': '59.99',
            'currency': 'USD',
            'max_attendees': 5,
            'session_type': 'online',
            'status': 'published'
        }
        response = self.client.post('/api/sessions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_session_as_user_fails(self):
        """Test creating session as user fails"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Session',
            'description': 'New Description',
            'category': 'Design',
            'duration_minutes': 90,
            'price': '59.99',
            'currency': 'USD',
            'max_attendees': 5,
            'session_type': 'online',
            'status': 'published'
        }
        response = self.client.post('/api/sessions/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookingTests(TestCase):
    """Test booking endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.creator = User.objects.create_user(
            username='creator',
            email='creator@example.com',
            password='testpass123',
            role='creator'
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123',
            role='user'
        )
        self.session = Session.objects.create(
            creator=self.creator,
            title='Test Session',
            description='Test Description',
            category='Programming',
            duration_minutes=60,
            price=Decimal('49.99'),
            currency='USD',
            max_attendees=10,
            session_type='online',
            status='published'
        )
    
    def test_create_booking(self):
        """Test creating a booking"""
        self.client.force_authenticate(user=self.user)
        data = {
            'session': self.session.id,
            'booking_date': timezone.now().isoformat(),
            'attendees_count': 2,
            'user_notes': 'Test booking'
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check total price calculation
        booking = Booking.objects.get(id=response.data['id'])
        expected_price = self.session.price * 2
        self.assertEqual(booking.total_price, expected_price)
    
    def test_booking_requires_authentication(self):
        """Test booking requires authentication"""
        data = {
            'session': self.session.id,
            'booking_date': timezone.now().isoformat(),
            'attendees_count': 1,
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_my_bookings(self):
        """Test listing user's bookings"""
        self.client.force_authenticate(user=self.user)
        
        # Create a booking
        Booking.objects.create(
            user=self.user,
            session=self.session,
            booking_date=timezone.now(),
            attendees_count=1,
            total_price=self.session.price
        )
        
        response = self.client.get('/api/bookings/my_bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class DashboardTests(TestCase):
    """Test dashboard endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.creator = User.objects.create_user(
            username='creator',
            email='creator@example.com',
            password='testpass123',
            role='creator'
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123',
            role='user'
        )
    
    def test_user_dashboard(self):
        """Test user dashboard access"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/dashboard/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('active_bookings', response.data)
        self.assertIn('past_bookings', response.data)
    
    def test_creator_dashboard(self):
        """Test creator dashboard access"""
        self.client.force_authenticate(user=self.creator)
        response = self.client.get('/api/dashboard/creator/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sessions', response.data)
        self.assertIn('stats', response.data)
    
    def test_creator_dashboard_user_forbidden(self):
        """Test user cannot access creator dashboard"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/dashboard/creator/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ModelTests(TestCase):
    """Test model methods and properties"""
    
    def setUp(self):
        self.creator = User.objects.create_user(
            username='creator',
            email='creator@example.com',
            password='testpass123',
            role='creator'
        )
        self.session = Session.objects.create(
            creator=self.creator,
            title='Test Session',
            description='Test Description',
            category='Programming',
            duration_minutes=60,
            price=Decimal('49.99'),
            currency='USD',
            max_attendees=10,
            session_type='online',
            status='published'
        )
    
    def test_session_is_available(self):
        """Test session is_available property"""
        self.assertTrue(self.session.is_available)
        
        self.session.status = 'draft'
        self.session.save()
        self.assertFalse(self.session.is_available)
    
    def test_booking_is_active(self):
        """Test booking is_active property"""
        user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123',
            role='user'
        )
        booking = Booking.objects.create(
            user=user,
            session=self.session,
            booking_date=timezone.now(),
            attendees_count=1,
            total_price=self.session.price,
            status='pending'
        )
        
        self.assertTrue(booking.is_active)
        
        booking.status = 'completed'
        booking.save()
        self.assertFalse(booking.is_active)
        self.assertTrue(booking.is_past)
