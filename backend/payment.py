import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from .models import Booking
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY


# Custom throttle for payment operations
class PaymentThrottle(UserRateThrottle):
    rate = '10/hour'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([PaymentThrottle])
def create_payment_intent(request):
    """
    Create a Stripe payment intent for a booking
    Rate limited to 10 requests per hour
    """
    booking_id = request.data.get('booking_id')
    
    if not booking_id:
        return Response(
            {'error': 'Booking ID is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.payment_status == 'paid':
        return Response(
            {'error': 'Booking already paid'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(booking.total_price * 100),  # Convert to cents
            currency=booking.session.currency.lower(),
            metadata={
                'booking_id': booking.id,
                'user_id': request.user.id,
                'session_id': booking.session.id,
            },
            automatic_payment_methods={
                'enabled': True,
            },
        )
        
        # Save payment intent ID
        booking.payment_intent_id = intent.id
        booking.save()
        
        return Response({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id,
        })
    
    except stripe.error.StripeError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([PaymentThrottle])
def confirm_payment(request):
    """
    Confirm payment after successful Stripe transaction
    Rate limited to 10 requests per hour
    """
    payment_intent_id = request.data.get('payment_intent_id')
    
    if not payment_intent_id:
        return Response(
            {'error': 'Payment intent ID is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            # Update booking
            booking = get_object_or_404(
                Booking,
                payment_intent_id=payment_intent_id,
                user=request.user
            )
            booking.payment_status = 'paid'
            booking.status = 'confirmed'
            booking.payment_method = intent.payment_method
            booking.save()
            
            return Response({
                'message': 'Payment confirmed successfully',
                'booking_id': booking.id,
            })
        else:
            return Response(
                {'error': 'Payment not completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except stripe.error.StripeError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def stripe_webhook(request):
    """
    Handle Stripe webhooks
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # Update booking
        try:
            booking = Booking.objects.get(
                payment_intent_id=payment_intent['id']
            )
            booking.payment_status = 'paid'
            booking.status = 'confirmed'
            booking.save()
        except Booking.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        # Update booking
        try:
            booking = Booking.objects.get(
                payment_intent_id=payment_intent['id']
            )
            booking.payment_status = 'failed'
            booking.save()
        except Booking.DoesNotExist:
            pass
    
    return Response(status=status.HTTP_200_OK)
