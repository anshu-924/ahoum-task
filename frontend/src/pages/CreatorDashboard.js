import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCreatorDashboard } from '../services/api';
import { useAuth } from '../context/AuthContext';
import SessionCard from '../components/SessionCard';
import BookingCard from '../components/BookingCard';
import './CreatorDashboard.css';

function CreatorDashboard() {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('sessions');

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const data = await getCreatorDashboard();
      console.log('Creator dashboard data:', data); // Debug log
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

  // Use the correct data from API response
  const allBookings = [
    ...(dashboard?.pending_bookings || []),
    ...(dashboard?.confirmed_bookings || [])
  ];
  
  const totalBookings = allBookings.length;
  const confirmedBookings = dashboard?.confirmed_bookings?.length || 0;
  const pendingBookings = dashboard?.pending_bookings?.length || 0;
  
  // Calculate revenue from confirmed bookings only
  const totalRevenue = (dashboard?.confirmed_bookings || [])
    .reduce((sum, b) => sum + parseFloat(b.total_price || 0), 0);

  return (
    <div className="dashboard creator-dashboard">
      <div className="container">
        <div className="dashboard-header">
          <div>
            <h1>Creator Dashboard</h1>
            <p>Welcome back, {user?.first_name || 'Creator'}!</p>
          </div>
          <Link to="/sessions/create" className="btn btn-primary">
            + Create New Session
          </Link>
        </div>

        {error && <div className="error">{error}</div>}

        <div className="dashboard-stats">
          <div className="stat-card card">
            <div className="stat-value">{dashboard?.sessions?.length || 0}</div>
            <div className="stat-label">Total Sessions</div>
          </div>
          <div className="stat-card card">
            <div className="stat-value">{totalBookings}</div>
            <div className="stat-label">Total Bookings</div>
          </div>
          <div className="stat-card card">
            <div className="stat-value">{confirmedBookings}</div>
            <div className="stat-label">Confirmed Bookings</div>
          </div>
          <div className="stat-card card">
            <div className="stat-value">${totalRevenue.toFixed(2)}</div>
            <div className="stat-label">Total Revenue</div>
          </div>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'sessions' ? 'active' : ''}`}
            onClick={() => setActiveTab('sessions')}
          >
            My Sessions ({dashboard?.sessions?.length || 0})
          </button>
          <button
            className={`tab ${activeTab === 'bookings' ? 'active' : ''}`}
            onClick={() => setActiveTab('bookings')}
          >
            Bookings ({totalBookings})
          </button>
          <button
            className={`tab ${activeTab === 'pending' ? 'active' : ''}`}
            onClick={() => setActiveTab('pending')}
          >
            Pending ({pendingBookings})
          </button>
        </div>

        {activeTab === 'sessions' && (
          <div className="dashboard-section">
            {dashboard?.sessions?.length === 0 ? (
              <div className="empty-state">
                <p>You haven't created any sessions yet.</p>
                <Link to="/sessions/create" className="btn btn-primary">
                  Create Your First Session
                </Link>
              </div>
            ) : (
              <div className="grid">
                {dashboard?.sessions?.map((session) => (
                  <SessionCard
                    key={session.id}
                    session={session}
                    showActions
                    onUpdate={fetchDashboard}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'bookings' && (
          <div className="dashboard-section">
            <h2>All Bookings</h2>
            {allBookings.length === 0 ? (
              <div className="empty-state">
                <p>No bookings yet for your sessions.</p>
              </div>
            ) : (
              <div className="bookings-list">
                {allBookings.map((booking) => (
                  <BookingCard
                    key={booking.id}
                    booking={booking}
                    isCreator
                    onUpdate={fetchDashboard}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'pending' && (
          <div className="dashboard-section">
            <h2>Pending Bookings - Require Confirmation</h2>
            {pendingBookings === 0 ? (
              <div className="empty-state">
                <p>No pending bookings to confirm.</p>
              </div>
            ) : (
              <div className="bookings-list">
                {(dashboard?.pending_bookings || []).map((booking) => (
                  <BookingCard
                    key={booking.id}
                    booking={booking}
                    isCreator
                    onUpdate={fetchDashboard}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default CreatorDashboard;
