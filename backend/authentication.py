from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import requests

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class OAuthProvider:
    """Base OAuth provider class"""
    
    @staticmethod
    def get_provider(provider_name):
        providers = {
            'google': GoogleOAuthProvider,
            'github': GitHubOAuthProvider,
        }
        return providers.get(provider_name.lower())


class GoogleOAuthProvider:
    """Google OAuth provider"""
    
    @staticmethod
    def get_user_info(access_token):
        """Fetch user info from Google"""
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise AuthenticationFailed(f'Failed to fetch user info from Google: {str(e)}')
    
    @staticmethod
    def create_or_update_user(user_info):
        """Create or update user from Google user info"""
        email = user_info.get('email')
        oauth_id = f"google_{user_info.get('id')}"
        
        user, created = User.objects.get_or_create(
            oauth_id=oauth_id,
            defaults={
                'username': email.split('@')[0],
                'email': email,
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'avatar': user_info.get('picture'),
                'oauth_provider': 'google',
                'bio': 'Student',
                'phone': '9876543210',
            }
        )
        
        # Update user info if not created
        if not created:
            user.first_name = user_info.get('given_name', user.first_name)
            user.last_name = user_info.get('family_name', user.last_name)
            user.avatar = user_info.get('picture', user.avatar)
            user.save()
        
        return user, created


class GitHubOAuthProvider:
    """GitHub OAuth provider"""
    
    @staticmethod
    def get_user_info(access_token):
        """Fetch user info from GitHub"""
        try:
            response = requests.get(
                'https://api.github.com/user',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            response.raise_for_status()
            user_data = response.json()
            
            # Get user email if not public
            if not user_data.get('email'):
                email_response = requests.get(
                    'https://api.github.com/user/emails',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                email_response.raise_for_status()
                emails = email_response.json()
                primary_email = next((e for e in emails if e.get('primary')), None)
                if primary_email:
                    user_data['email'] = primary_email.get('email')
            
            return user_data
        except Exception as e:
            raise AuthenticationFailed(f'Failed to fetch user info from GitHub: {str(e)}')
    
    @staticmethod
    def create_or_update_user(user_info):
        """Create or update user from GitHub user info"""
        email = user_info.get('email')
        oauth_id = f"github_{user_info.get('id')}"
        
        # Split name if available
        name = user_info.get('name', '')
        name_parts = name.split(' ', 1) if name else ['', '']
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        user, created = User.objects.get_or_create(
            oauth_id=oauth_id,
            defaults={
                'username': user_info.get('login'),
                'email': email or f"{user_info.get('login')}@github.local",
                'first_name': first_name,
                'last_name': last_name,
                'avatar': user_info.get('avatar_url'),
                'oauth_provider': 'github',
                'bio': user_info.get('bio') or 'Student',
                'phone': '',
            }
        )
        
        # Update user info if not created
        if not created:
            user.first_name = first_name or user.first_name
            user.last_name = last_name or user.last_name
            user.avatar = user_info.get('avatar_url', user.avatar)
            # Only update bio if GitHub provides one, otherwise keep existing
            github_bio = user_info.get('bio')
            if github_bio:
                user.bio = github_bio
            user.save()
        
        return user, created
