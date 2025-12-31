import React, { useState, useEffect } from 'react';
import { getUserDashboard } from '../services/api';
import { useAuth } from '../context/AuthContext';
import BookingCard from '../components/BookingCard';
import './UserDashboard.css';

function UserDashboard() {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const data = await getUserDashboard();
      console.log('Dashboard data:', data); // Debug log
      setDashboard(data);
    } catch (err) {
      setError('Failed to load dashboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container loading">Loading dashboard...</div>;
  }

  // Use active_bookings from API response
  const bookings = dashboard?.active_bookings || [];
  const totalBookings = bookings.length;
  const confirmedCount = bookings.filter((b) => b.status === 'confirmed').length;
  const pendingCount = bookings.filter((b) => b.status === 'pending').length;

  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <div>
            <h1>My Enrollments</h1>
            <p>Welcome, {user?.first_name || 'Student'}! Here are your enrolled sessions</p>
          </div>
          <a href="/" className="btn btn-primary">
            Browse More Sessions
          </a>
        </div>

        {error && <div className="error">{error}</div>}

        <div className="dashboard-stats">
          <div className="stat-card card">
            <div className="stat-value">{totalBookings}</div>
            <div className="stat-label">Total Enrollments</div>
          </div>
          <div className="stat-card card">
            <div className="stat-value">{confirmedCount}</div>
            <div className="stat-label">Confirmed</div>
          </div>
          <div className="stat-card card">
            <div className="stat-value">{pendingCount}</div>
            <div className="stat-label">Pending</div>
          </div>
        </div>

        <div className="dashboard-section">
          <h2>My Enrolled Sessions</h2>
          {bookings.length === 0 ? (
            <div className="empty-state">
              <p>You haven't enrolled in any sessions yet.</p>
              <a href="/" className="btn btn-primary">
                Browse Available Sessions
              </a>
            </div>
          ) : (
            <div className="bookings-list">
              {bookings.map((booking) => (
                <BookingCard key={booking.id} booking={booking} onUpdate={fetchDashboard} />
              ))}
            </div>
          )}
        </div>

        <div className="dashboard-section">
          <h2>Profile</h2>
          <div className="card profile-card">
            <div className="profile-info">
              <div className="profile-item">
                <strong>Email:</strong> {user?.email}
              </div>
              <div className="profile-item">
                <strong>Name:</strong> {user?.first_name} {user?.last_name}
              </div>
              <div className="profile-item">
                <strong>Role:</strong> {user?.role}
              </div>
              {user?.bio && (
                <div className="profile-item">
                  <strong>Bio:</strong> {user?.bio}
                </div>
              )}
            </div>
            <a href="/profile" className="btn btn-outline">
              Edit Profile
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;
