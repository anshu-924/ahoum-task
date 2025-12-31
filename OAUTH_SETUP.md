# OAuth Login Setup - Final Steps

## ✅ What's Already Done

The OAuth authentication is now fully implemented in the code:

1. **Backend**: 
   - Google OAuth login endpoint
   - GitHub code exchange endpoint
   - User creation/update from OAuth data

2. **Frontend**:
   - Google Sign-In with Google Identity Services
   - GitHub OAuth with authorization code flow
   - Token storage and auto-refresh

## 🔧 What You Need to Do

### 1. Configure Google OAuth Redirect URIs

Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials):
- Select your project
- Click on your OAuth 2.0 Client ID
- Under "Authorized JavaScript origins", add:
  - `http://localhost:3000` (for development)
  - `http://localhost` (for production)
- Under "Authorized redirect URIs", add:
  - `http://localhost:3000/login` (for development)
  - `http://localhost/login` (for production)
- Click "Save"

### 2. Configure GitHub OAuth Redirect URIs

Go to [GitHub Developer Settings](https://github.com/settings/developers):
- Click on your OAuth App
- Under "Authorization callback URL", you can only set ONE URL. Set it to:
  - `http://localhost:3000/login` (for development)
  - **OR** `http://localhost/login` (for production after docker deployment)
- Click "Update application"

**Note**: For GitHub, you'll need to change this URL when switching between development and production, or create two separate OAuth apps (one for dev, one for prod).

### 3. Restart Docker Containers

After configuring the redirect URIs:

```bash
docker-compose down
docker-compose up --build
```

## 🧪 How to Test

1. **Open the app**: http://localhost

2. **Test Google Login**:
   - Click "Login with Google"
   - Select role (User/Creator)
   - Sign in with your Google account
   - You should be redirected to the dashboard

3. **Test GitHub Login**:
   - Click "Login with GitHub"
   - Select role (User/Creator)
   - Authorize the app
   - You should be redirected to the dashboard

4. **Verify**:
   - Check that your profile shows correct info
   - Try creating a session (if creator)
   - Try booking a session (if user)
   - Logout and login again to test token persistence

## 🐛 Troubleshooting

**"redirect_uri_mismatch" error**: 
- Make sure the redirect URI in OAuth provider settings exactly matches `http://localhost/login`

**"Failed to get access token" error**:
- Check browser console for detailed errors
- Verify your client IDs are correct in `.env` file
- Make sure the backend container has access to the environment variables

**Google Sign-In not loading**:
- Refresh the page
- Check browser console for script loading errors
- Ensure you have internet connection (Google SDK loads from CDN)

**GitHub popup blocked**:
- Allow popups for localhost in your browser
- Try right-clicking the GitHub button and "Open in new tab"

## 📝 Demo Login (Optional)

For testing without OAuth, there's still a "Demo Login" button that creates a temporary session. This is useful for:
- Testing UI without OAuth setup
- Development when offline
- Quick feature testing

**Note**: Demo login won't persist after page refresh and won't create real database records.
