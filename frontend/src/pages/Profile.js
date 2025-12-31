import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getCurrentUser, updateProfile } from '../services/api';
import './Profile.css';

function Profile() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    bio: '',
    phone: '',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        bio: user.bio || '',
        phone: user.phone || '',
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await updateProfile(formData);
      const updatedUser = await getCurrentUser();
      login({ access: localStorage.getItem('access_token'), refresh: localStorage.getItem('refresh_token') }, updatedUser);
      setSuccess(true);
      setIsEditing(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="profile-page">
      <div className="container">
        <div className="profile-container card">
          <div className="profile-header">
            <h1>Profile</h1>
            <button
              className="btn btn-outline"
              onClick={() => navigate(user?.role === 'creator' ? '/creator/dashboard' : '/dashboard')}
            >
              Back to Dashboard
            </button>
          </div>

          {success && <div className="success">Profile updated successfully!</div>}
          {error && <div className="error">{error}</div>}

          {!isEditing ? (
            <div className="profile-view">
              <div className="profile-details">
                <div className="detail-item">
                  <strong>Email:</strong>
                  <span>{user?.email}</span>
                </div>
                <div className="detail-item">
                  <strong>First Name:</strong>
                  <span>{user?.first_name || 'Not set'}</span>
                </div>
                <div className="detail-item">
                  <strong>Last Name:</strong>
                  <span>{user?.last_name || 'Not set'}</span>
                </div>
                <div className="detail-item">
                  <strong>Phone:</strong>
                  <span>{user?.phone || 'Not set'}</span>
                </div>
                <div className="detail-item">
                  <strong>Role:</strong>
                  <span>{user?.role === 'creator' ? 'Tutor' : 'Student'}</span>
                </div>
                <div className="detail-item">
                  <strong>Bio:</strong>
                  <span>{user?.bio || 'No bio added yet'}</span>
                </div>
              </div>
              <button
                className="btn btn-primary"
                onClick={() => setIsEditing(true)}
              >
                Edit Profile
              </button>
            </div>
          ) : (
            <div className="profile-edit">
              <h2>Edit Profile</h2>
              <p className="subtitle">Update your personal information</p>

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Email</label>
                  <input type="email" value={user?.email || ''} disabled />
                  <small>Email cannot be changed</small>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>First Name</label>
                    <input
                      type="text"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Last Name</label>
                    <input
                      type="text"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Phone</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="+1234567890"
                  />
                </div>

                <div className="form-group">
                  <label>Bio</label>
                  <textarea
                    name="bio"
                    rows="4"
                    value={formData.bio}
                    onChange={handleChange}
                    placeholder="Tell us about yourself..."
                  />
                </div>

                <div className="form-actions">
                  <button
                    type="button"
                    className="btn btn-outline"
                    onClick={() => setIsEditing(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Profile;
