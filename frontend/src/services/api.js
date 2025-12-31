import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication
export const oauthLogin = async (provider, accessToken, role) => {
  const response = await api.post('/auth/oauth/login/', {
    provider,
    access_token: accessToken,
    role,
  });
  return response.data;
};

export const githubCodeExchange = async (code, role) => {
  const response = await api.post('/auth/github/callback/', {
    code,
    role,
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/users/me/');
  return response.data;
};

export const updateProfile = async (data) => {
  const response = await api.put('/users/update_profile/', data);
  return response.data;
};

// Sessions
export const getSessions = async () => {
  const response = await api.get('/sessions/');
  return response.data;
};

export const getSessionDetail = async (id) => {
  const response = await api.get(`/sessions/${id}/`);
  return response.data;
};

export const createSession = async (data) => {
  const response = await api.post('/sessions/', data);
  return response.data;
};

export const updateSession = async (id, data) => {
  const response = await api.put(`/sessions/${id}/`, data);
  return response.data;
};

export const deleteSession = async (id) => {
  const response = await api.delete(`/sessions/${id}/`);
  return response.data;
};

export const getMySessions = async () => {
  const response = await api.get('/sessions/my_sessions/');
  return response.data;
};

// Bookings
export const createBooking = async (data) => {
  const response = await api.post('/bookings/', data);
  return response.data;
};

export const getMyBookings = async () => {
  const response = await api.get('/bookings/my_bookings/');
  return response.data;
};

export const getActiveBookings = async () => {
  const response = await api.get('/bookings/active/');
  return response.data;
};

export const confirmBooking = async (id) => {
  const response = await api.post(`/bookings/${id}/confirm/`);
  return response.data;
};

export const cancelBooking = async (id) => {
  const response = await api.post(`/bookings/${id}/cancel/`);
  return response.data;
};

// Dashboards
export const getUserDashboard = async () => {
  const response = await api.get('/dashboard/user/');
  return response.data;
};

export const getCreatorDashboard = async () => {
  const response = await api.get('/dashboard/creator/');
  return response.data;
};

export default api;
