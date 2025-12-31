import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import SessionDetail from './pages/SessionDetail';
import UserDashboard from './pages/UserDashboard';
import CreatorDashboard from './pages/CreatorDashboard';
import Profile from './pages/Profile';
import CreateSession from './pages/CreateSession';
import EditSession from './pages/EditSession';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/sessions/:id" element={<SessionDetail />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute requireStudent>
                <UserDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/creator/dashboard"
            element={
              <PrivateRoute requireCreator>
                <CreatorDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          />
          <Route
            path="/sessions/create"
            element={
              <PrivateRoute requireCreator>
                <CreateSession />
              </PrivateRoute>
            }
          />
          <Route
            path="/sessions/:id/edit"
            element={
              <PrivateRoute requireCreator>
                <EditSession />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
