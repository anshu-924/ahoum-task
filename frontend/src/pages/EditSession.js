import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSessionDetail, updateSession } from '../services/api';
import './CreateSession.css';

function EditSession() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    description: '',
    location: '',
    session_type: 'online',
    max_attendees: 10,
    status: 'published',
  });
  const [sessionInfo, setSessionInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchSession();
  }, [id]);

  const fetchSession = async () => {
    try {
      const data = await getSessionDetail(id);
      setSessionInfo(data);
      setFormData({
        description: data.description || '',
        location: data.location || '',
        session_type: data.session_type || 'online',
        max_attendees: data.max_attendees || 10,
        status: data.status || 'published',
      });
    } catch (err) {
      setError('Failed to load session details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(false);

    try {
      await updateSession(id, formData);
      setSuccess(true);
      setTimeout(() => {
        navigate('/creator/dashboard');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update session');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (e) => {
    const value = e.target.type === 'number' ? parseInt(e.target.value) : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  if (loading) {
    return <div className="container loading">Loading session...</div>;
  }

  return (
    <div className="create-session-page">
      <div className="container">
        <div className="create-session-container card">
          <h1>Edit Session</h1>
          <p className="subtitle">Update session details (some fields cannot be changed)</p>

          {/* Non-editable fields display */}
          <div className="session-info-display">
            <div className="info-item">
              <strong>Title:</strong> {sessionInfo?.title}
            </div>
            <div className="info-item">
              <strong>Category:</strong> {sessionInfo?.category}
            </div>
            <div className="info-item">
              <strong>Duration:</strong> {sessionInfo?.duration_minutes} minutes
            </div>
            <div className="info-item">
              <strong>Price:</strong> ${sessionInfo?.price} {sessionInfo?.currency}
            </div>
            <small style={{ color: '#666', marginTop: '10px', display: 'block' }}>
              * Title, Category, Duration, and Price cannot be changed after creation
            </small>
          </div>

          <hr style={{ margin: '20px 0', border: 'none', borderTop: '1px solid #ddd' }} />

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Description *</label>
              <textarea
                name="description"
                rows="5"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe what students will learn..."
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Session Type *</label>
                <select name="session_type" value={formData.session_type} onChange={handleChange}>
                  <option value="online">Online</option>
                  <option value="in-person">In-Person</option>
                  <option value="hybrid">Hybrid</option>
                </select>
              </div>

              <div className="form-group">
                <label>Max Attendees *</label>
                <input
                  type="number"
                  name="max_attendees"
                  value={formData.max_attendees}
                  onChange={handleChange}
                  min="1"
                  max="100"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Location *</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g., Zoom meeting link or physical address"
                required
              />
            </div>

            <div className="form-group">
              <label>Status *</label>
              <select name="status" value={formData.status} onChange={handleChange}>
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="cancelled">Cancelled</option>
              </select>
              <small>Draft sessions are not visible to students</small>
            </div>

            {error && <div className="error">{error}</div>}
            {success && <div className="success">Session updated successfully!</div>}

            <div className="form-actions">
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => navigate('/creator/dashboard')}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default EditSession;
