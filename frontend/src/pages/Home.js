import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getSessions, getUserDashboard } from '../services/api';
import SessionCard from '../components/SessionCard';
import { useAuth } from '../context/AuthContext';
import './Home.css';

function Home() {
  const { isAuthenticated, isCreator, isStudent } = useAuth();
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [enrolledSessionIds, setEnrolledSessionIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchSessions();
    if (isAuthenticated && isStudent) {
      fetchEnrolledSessions();
    }
  }, [isAuthenticated, isStudent]);

  const fetchSessions = async () => {
    try {
      const data = await getSessions();
      // Handle paginated response with results array or direct array
      const sessionsList = data?.results || (Array.isArray(data) ? data : []);
      setSessions(sessionsList);
    } catch (err) {
      setError('Failed to load sessions');
      console.error(err);
      setSessions([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchEnrolledSessions = async () => {
    try {
      const data = await getUserDashboard();
      // Extract session IDs from active bookings
      const enrolledIds = (data?.active_bookings || []).map(booking => booking.session);
      setEnrolledSessionIds(enrolledIds);
    } catch (err) {
      console.error('Failed to fetch enrolled sessions:', err);
    }
  };

  const filteredSessions = sessions.filter((session) => {
    if (filter === 'all') return true;
    return session.category.toLowerCase() === filter.toLowerCase();
  });

  const categories = ['all', ...new Set(sessions.map((s) => s.category))];

  // Redirect creators to their dashboard
  useEffect(() => {
    if (isAuthenticated && isCreator) {
      navigate('/creator/dashboard');
    }
  }, [isAuthenticated, isCreator, navigate]);

  return (
    <div className="home">
      <div className="hero">
        <div className="container">
          <h1>{isStudent ? 'Available Sessions' : 'Discover Amazing Sessions'}</h1>
          <p>{isStudent ? 'Enroll in sessions from expert tutors' : 'Browse and book sessions from expert creators'}</p>
          {!isAuthenticated && (
            <Link to="/login" className="btn btn-primary">
              Get Started
            </Link>
          )}
        </div>
      </div>

      <div className="container">
        <div className="filters">
          <h2>{isStudent ? 'Available Sessions' : 'Browse Sessions'}</h2>
          <div className="filter-buttons">
            {categories.map((category) => (
              <button
                key={category}
                className={`btn ${filter === category ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setFilter(category)}
              >
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {loading && <div className="loading">Loading sessions...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && !error && (
          <div className="grid">
            {filteredSessions.map((session) => (
              <SessionCard 
                key={session.id} 
                session={session}
                showEnrollButton={isStudent}
                isEnrolled={enrolledSessionIds.includes(session.id)}
              />
            ))}
          </div>
        )}

        {!loading && !error && filteredSessions.length === 0 && (
          <div className="no-sessions">
            <p>No sessions found in this category.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;
