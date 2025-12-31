import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { oauthLogin, githubCodeExchange } from '../services/api';
import './Login.css';

function Login() {
  const [role, setRole] = useState('user');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { login } = useAuth();
  const navigate = useNavigate();

  const GOOGLE_CLIENT_ID = '256952312824-4og6bbf32p58178ojqm642gfkgv795ro.apps.googleusercontent.com';
  const GITHUB_CLIENT_ID = 'Ov23li7bXC4RlozzV9qR';
  // Use current origin for redirect (works with localhost:3000 dev or localhost prod)
  const REDIRECT_URI = window.location.origin + '/login';

  useEffect(() => {
    // Load Google Sign-In script
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onerror = () => {
      console.error('Failed to load Google Sign-In script');
      setError('Failed to load Google Sign-In. Check your internet connection.');
    };
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const handleGoogleLogin = () => {
    setLoading(true);
    setError(null);

    if (window.google) {
      const client = window.google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_CLIENT_ID,
        scope: 'email profile',
        callback: async (response) => {
          if (response.error) {
            // User closed the popup or denied access
            console.log('Google login cancelled:', response.error);
            setLoading(false);
            if (response.error !== 'popup_closed' && response.error !== 'access_denied') {
              setError('Google login failed: ' + response.error);
            }
            return;
          }
          
          if (response.access_token) {
            try {
              const result = await oauthLogin('google', response.access_token, role);
              login(result.tokens, result.user);
              navigate(role === 'creator' ? '/creator/dashboard' : '/dashboard');
            } catch (err) {
              setError(err.response?.data?.error || 'Google login failed');
              setLoading(false);
            }
          } else {
            setError('Failed to get Google access token');
            setLoading(false);
          }
        },
      });
      client.requestAccessToken();
    } else {
      setError('Google Sign-In not loaded. Please refresh and try again.');
      setLoading(false);
    }
  };

  const handleGitHubLogin = () => {
    setLoading(true);
    setError(null);

    const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=user:email&state=${role}`;
    
    // Open GitHub OAuth in popup
    const width = 600;
    const height = 700;
    const left = window.screen.width / 2 - width / 2;
    const top = window.screen.height / 2 - height / 2;
    
    const popup = window.open(
      githubAuthUrl,
      'GitHub Login',
      `width=${width},height=${height},left=${left},top=${top}`
    );

    // Listen for OAuth callback
    let hasReceivedCode = false;
    const checkPopup = setInterval(() => {
      try {
        if (popup.closed) {
          clearInterval(checkPopup);
          if (!hasReceivedCode) {
            // User closed popup without completing login
            setLoading(false);
          }
          return;
        }
        
        if (popup.location.href.includes(REDIRECT_URI)) {
          const params = new URLSearchParams(popup.location.search);
          const code = params.get('code');
          
          if (code) {
            hasReceivedCode = true;
            clearInterval(checkPopup);
            popup.close();
            handleGitHubCallback(code);
          }
        }
      } catch (err) {
        // Cross-origin error - popup still on GitHub domain
      }
    }, 500);
  };

  const handleGitHubCallback = async (code) => {
    try {
      // Exchange code for access token via backend
      const result = await githubCodeExchange(code, role);
      login(result.tokens, result.user);
      navigate(role === 'creator' ? '/creator/dashboard' : '/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'GitHub login failed');
    } finally {
      setLoading(false);
    }
  };

  // Demo login function (for development/testing only)
  const handleDemoLogin = async () => {
    setLoading(true);
    setError(null);

    try {
      // This is a demo function - in production, remove this
      // and only use actual OAuth flow
      const demoToken = 'demo-token-' + Date.now();
      
      // Mock login - replace with actual OAuth
      const response = {
        tokens: {
          access: demoToken,
          refresh: 'refresh-' + demoToken,
        },
        user: {
          id: 1,
          email: role === 'creator' ? 'creator@demo.com' : 'user@demo.com',
          first_name: role === 'creator' ? 'Demo Creator' : 'Demo User',
          role: role,
        },
      };

      login(response.tokens, response.user);
      navigate(role === 'creator' ? '/creator/dashboard' : '/dashboard');
    } catch (err) {
      setError('Demo login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="container">
        <div className="login-card card">
          <h1>Welcome to Sessions Marketplace</h1>
          <p className="subtitle">Sign in to access your account</p>

          <div className="role-selector">
            <h3>Select Your Role</h3>
            <div className="role-buttons">
              <button
                className={`role-btn ${role === 'user' ? 'active' : ''}`}
                onClick={() => setRole('user')}
              >
                <div className="role-icon">👤</div>
                <div className="role-title">Student</div>
                <div className="role-desc">Browse and book sessions</div>
              </button>
              <button
                className={`role-btn ${role === 'creator' ? 'active' : ''}`}
                onClick={() => setRole('creator')}
              >
                <div className="role-icon">🎓</div>
                <div className="role-title">Tutor</div>
                <div className="role-desc">Create and manage sessions</div>
              </button>
            </div>
          </div>

          {error && <div className="error">{error}</div>}

          <div className="oauth-buttons">
            <button
              className="oauth-btn google"
              onClick={handleGoogleLogin}
              disabled={loading}
            >
              <span>🔵</span> Continue with Google
            </button>
            <button
              className="oauth-btn github"
              onClick={handleGitHubLogin}
              disabled={loading}
            >
              <span>⚫</span> Continue with GitHub
            </button>
          </div>

          <div className="demo-section">
            <hr />
            <p className="demo-label">For Testing/Demo</p>
            <button
              className="btn btn-secondary"
              onClick={handleDemoLogin}
              disabled={loading}
            >
              {loading ? 'Logging in...' : 'Demo Login'}
            </button>
            <p className="demo-note">
              Demo login creates a temporary session for testing purposes
            </p>
          </div>

          <div className="oauth-setup-note">
            <p>
              <strong>Note:</strong> To use OAuth login, you need to set up OAuth credentials.
              See the README for setup instructions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
