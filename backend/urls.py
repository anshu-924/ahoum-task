from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    oauth_login, github_code_exchange, logout,
    UserViewSet, SessionViewSet, BookingViewSet,
    user_dashboard, creator_dashboard
)
from .payment import create_payment_intent, confirm_payment, stripe_webhook
from .storage import upload_file, delete_file

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # Authentication
    path('auth/oauth/login/', oauth_login, name='oauth-login'),
    path('auth/github/callback/', github_code_exchange, name='github-callback'),
    path('auth/logout/', logout, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Dashboards
    path('dashboard/user/', user_dashboard, name='user-dashboard'),
    path('dashboard/creator/', creator_dashboard, name='creator-dashboard'),
    
    # Payment (Bonus)
    path('payment/create-intent/', create_payment_intent, name='create-payment-intent'),
    path('payment/confirm/', confirm_payment, name='confirm-payment'),
    path('payment/webhook/', stripe_webhook, name='stripe-webhook'),
    
    # File Storage (Bonus)
    path('storage/upload/', upload_file, name='upload-file'),
    path('storage/delete/', delete_file, name='delete-file'),
    
    # Router URLs
    path('', include(router.urls)),
]


