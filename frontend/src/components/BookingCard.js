import React, { useState } from 'react';
import { confirmBooking, cancelBooking } from '../services/api';
import './BookingCard.css';

function BookingCard({ booking, isCreator, onUpdate }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleConfirm = async () => {
    setLoading(true);
    setError(null);
    try {
      await confirmBooking(booking.id);
      onUpdate && onUpdate();
    } catch (err) {
      setError('Failed to confirm booking');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async () => {
    if (window.confirm('Are you sure you want to cancel this booking?')) {
      setLoading(true);
      setError(null);
      try {
        await cancelBooking(booking.id);
        onUpdate && onUpdate();
      } catch (err) {
        setError('Failed to cancel booking');
      } finally {
        setLoading(false);
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: '#ff9800',
      confirmed: '#4caf50',
      cancelled: '#f44336',
      completed: '#2196f3',
    };
    return colors[status] || '#666666';
  };

  return (
    <div className="booking-card card">
      <div className="booking-header">
        <div>
          <h3>{booking.session_title}</h3>
          <p className="booking-meta">
            📅 {formatDate(booking.booking_date)}
          </p>
        </div>
        <div
          className="status-badge"
          style={{ backgroundColor: getStatusColor(booking.status) }}
        >
          {booking.status}
        </div>
      </div>

      <div className="booking-details">
        {isCreator ? (
          <>
            <div className="detail-row">
              <strong>Student:</strong> {booking.user_name}
            </div>
            <div className="detail-row">
              <strong>Email:</strong> {booking.user_email}
            </div>
          </>
        ) : (
          <div className="detail-row">
            <strong>Creator:</strong> {booking.creator_name}
          </div>
        )}
        <div className="detail-row">
          <strong>Attendees:</strong> {booking.attendees_count}
        </div>
        <div className="detail-row">
          <strong>Total Price:</strong> ${booking.total_price} {booking.currency}
        </div>
        {booking.user_notes && (
          <div className="detail-row">
            <strong>Notes:</strong> {booking.user_notes}
          </div>
        )}
      </div>

      {error && <div className="error">{error}</div>}

      <div className="booking-actions">
        {isCreator && booking.status === 'pending' && (
          <button
            className="btn btn-primary"
            onClick={handleConfirm}
            disabled={loading}
          >
            Confirm Booking
          </button>
        )}
        {booking.status !== 'cancelled' && booking.status !== 'completed' && (
          <button
            className="btn btn-secondary"
            onClick={handleCancel}
            disabled={loading}
          >
            Cancel Booking
          </button>
        )}
      </div>
    </div>
  );
}

export default BookingCard;
