import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
  const { user, isAuthenticated, isCreator, isStudent, logout } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  return (
    <nav>
      <div className="container">
        <Link to="/" className="logo">
          <h1>Sessions Marketplace</h1>
        </Link>

        <div className="nav-links">
          {isAuthenticated ? (
            <>
              {isCreator ? (
                <>
                  <Link to="/creator/dashboard">Dashboard</Link>
                  <Link to="/sessions/create">Create Session</Link>
                </>
              ) : isStudent ? (
                <>
                  <Link to="/">Available Sessions</Link>
                  <Link to="/dashboard">My Enrollments</Link>
                </>
              ) : (
                <Link to="/dashboard">Dashboard</Link>
              )}
              <Link to="/profile">Profile</Link>
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/">Browse</Link>
              <Link to="/login">
                <button>Login</button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
