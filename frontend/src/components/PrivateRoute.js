import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function PrivateRoute({ children, requireCreator, requireStudent }) {
  const { isAuthenticated, isCreator, isStudent, loading } = useAuth();

  if (loading) {
    return <div className="container loading">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (requireCreator && !isCreator) {
    return <Navigate to="/dashboard" />;
  }

  if (requireStudent && !isStudent) {
    return <Navigate to="/creator/dashboard" />;
  }

  return children;
}

export default PrivateRoute;
