from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    """
    Permission to only allow creators to access certain views
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'creator'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit objects
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the creator of the session
        return obj.creator == request.user


class IsBookingOwnerOrSessionCreator(permissions.BasePermission):
    """
    Permission to allow booking owner or session creator to access booking
    """
    
    def has_object_permission(self, request, view, obj):
        # Booking owner can access their booking
        if obj.user == request.user:
            return True
        
        # Session creator can access bookings for their session
        if obj.session.creator == request.user:
            return True
        
        return False
