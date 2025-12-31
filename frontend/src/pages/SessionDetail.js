import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSessionDetail, createBooking, getUserDashboard } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './SessionDetail.css';

function SessionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, isStudent, isCreator } = useAuth();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userNotes, setUserNotes] = useState('');
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingSuccess, setBookingSuccess] = useState(false);
  const [isEnrolled, setIsEnrolled] = useState(false);

  useEffect(() => {
    fetchSession();
    if (isAuthenticated && isStudent) {
      checkEnrollmentStatus();
    }
  }, [id, isAuthenticated, isStudent]);

  const fetchSession = async () => {
    try {
      const data = await getSessionDetail(id);
      setSession(data);
    } catch (err) {
      setError('Failed to load session details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const checkEnrollmentStatus = async () => {
    try {
      const data = await getUserDashboard();
      const enrolledIds = (data?.active_bookings || []).map(booking => booking.session);
      setIsEnrolled(enrolledIds.includes(parseInt(id)));
    } catch (err) {
      console.error('Failed to check enrollment:', err);
    }
  };

  const handleBooking = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (isCreator) {
      setError('Tutors cannot enroll in sessions. Please log in as a student.');
      return;
    }

    setBookingLoading(true);
    setError(null);

    try {
      // Create booking with default values
      const bookingData = {
        session: parseInt(id),
        booking_date: new Date().toISOString(), // Current date/time in ISO format
        attendees_count: 1, // Default to 1 attendee
        user_notes: userNotes || '', // Optional notes
      };
      
      await createBooking(bookingData);
      setBookingSuccess(true);
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to enroll in session');
    } finally {
      setBookingLoading(false);
    }
  };

  if (loading) {
    return <div className="container loading">Loading session...</div>;
  }

  if (error && !session) {
    return (
      <div className="container">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="session-detail">
      <div className="container">
        <button className="btn btn-outline back-btn" onClick={() => navigate('/')}>
          ← Back to Sessions
        </button>

        <div className="detail-grid">
          <div className="detail-content">
            <div className="session-image-container">
              <img 
                src={session.image_url || session.thumbnail_url || '/image/thumbnail_temmplate.jpg'} 
                alt={session.title}
                className="session-detail-image"
                onError={(e) => {
                  e.target.src = '/image/thumbnail_temmplate.jpg';
                }}
              />
            </div>
            
            <div className="session-header">
              <span className="category-badge">{session.category}</span>
              <h1>{session.title}</h1>
              <div className="session-meta">
                <span>👤 {session.creator_name}</span>
                <span>⏱️ {session.duration_minutes} minutes</span>
                <span>📍 {session.location}</span>
              </div>
            </div>

            <div className="session-description">
              <h2>About This Session</h2>
              <p>{session.description}</p>
            </div>

            <div className="session-details">
              <h2>Details</h2>
              <div className="detail-item">
                <strong>Type:</strong> {session.session_type}
              </div>
              <div className="detail-item">
                <strong>Max Attendees:</strong> {session.max_attendees}
              </div>
              <div className="detail-item">
                <strong>Status:</strong> {session.status}
              </div>
            </div>
          </div>

          <div className="booking-sidebar">
            <div className="card booking-card">
              <div className="price">
                <span className="amount">${session.price}</span>
                <span className="currency">{session.currency}</span>
              </div>

              {isCreator ? (
                <div className="info-message">
                  <p>You are logged in as a tutor. Students can enroll in your sessions.</p>
                </div>
              ) : isEnrolled ? (
                <div className="success" style={{ padding: '20px', textAlign: 'center' }}>
                  <h3>✓ Already Enrolled</h3>
                  <p>You are already enrolled in this session.</p>
                  <button
                    className="btn btn-primary"
                    onClick={() => navigate('/dashboard')}
                    style={{ marginTop: '10px' }}
                  >
                    View My Enrollments
                  </button>
                </div>
              ) : bookingSuccess ? (
                <div className="success">
                  ✓ Enrollment successful! Redirecting to your dashboard...
                </div>
              ) : (
                <form onSubmit={handleBooking}>
                  <div className="enrollment-info">
                    <p><strong>Quick Enrollment</strong></p>
                    <p>Click below to enroll in this session instantly.</p>
                  </div>

                  <div className="form-group">
                    <label>Notes (Optional)</label>
                    <textarea
                      rows="3"
                      value={userNotes}
                      onChange={(e) => setUserNotes(e.target.value)}
                      placeholder="Any special requests or questions?"
                      disabled={!isAuthenticated}
                    />
                  </div>

                  {error && <div className="error">{error}</div>}

                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={bookingLoading || !isAuthenticated}
                  >
                    {!isAuthenticated ? 'Login to Enroll' : bookingLoading ? 'Enrolling...' : 'Enroll Now'}
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SessionDetail;
