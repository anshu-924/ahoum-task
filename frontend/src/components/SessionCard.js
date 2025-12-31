import React from 'react';
import { Link } from 'react-router-dom';
import './SessionCard.css';

function SessionCard({ session, showActions, onUpdate, showEnrollButton, isEnrolled }) {
  // Use uploaded thumbnail or default image
  const thumbnailUrl = session.thumbnail_url || '/image/thumbnail_temmplate.jpg';
  
  return (
    <div className="session-card card">
      <div className="session-thumbnail">
        <img 
          src={thumbnailUrl} 
          alt={session.title}
          onError={(e) => {
            e.target.src = '/image/thumbnail_temmplate.jpg';
          }}
        />
      </div>
      
      <div className="session-card-header">
        <span className="category-badge">{session.category}</span>
        <span className="status-badge status-{session.status}">{session.status}</span>
        {isEnrolled && (
          <span className="enrolled-badge" style={{ backgroundColor: '#4caf50', color: 'white', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>✓ Enrolled</span>
        )}
      </div>

      <h3>{session.title}</h3>
      <p className="description">{session.description.substring(0, 100)}...</p>

      <div className="session-meta">
        <span>👤 {session.creator_name}</span>
        <span>⏱️ {session.duration_minutes}m</span>
      </div>

      <div className="session-footer">
        <div className="price">
          <span className="amount">${session.price}</span>
          <span className="currency">{session.currency}</span>
        </div>

        <Link to={`/sessions/${session.id}`} className="btn btn-primary">
          {isEnrolled ? 'View Details' : showEnrollButton ? 'Enroll Now' : 'View Details'}
        </Link>
      </div>

      {showActions && (
        <div className="session-actions">
          <Link to={`/sessions/${session.id}/edit`} className="btn btn-outline btn-sm">
            ✏️ Edit
          </Link>
        </div>
      )}
    </div>
  );
}

export default SessionCard;
