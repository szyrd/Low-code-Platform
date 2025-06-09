import axios, { AxiosResponse } from 'axios';
import { LayoutData } from '../types/types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Token management
let accessToken: string | null = null;
let refreshToken: string | null = null;

// Axios instance with interceptors
const api = axios.create({
  baseURL: API_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
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
      
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          
          accessToken = response.data.access;
          setTokens(accessToken, refreshToken);
          
          // Retry original request
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, logout user
          logout();
          return Promise.reject(refreshError);
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// Token management functions
export const setTokens = (access: string, refresh: string) => {
  accessToken = access;
  refreshToken = refresh;
  
  // Store in localStorage for persistence
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
};

export const clearTokens = () => {
  accessToken = null;
  refreshToken = null;
  
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

export const loadTokensFromStorage = () => {
  const storedAccess = localStorage.getItem('accessToken');
  const storedRefresh = localStorage.getItem('refreshToken');
  
  if (storedAccess && storedRefresh) {
    accessToken = storedAccess;
    refreshToken = storedRefresh;
  }
};

// Authentication functions
export const login = async (username: string, password: string) => {
  try {
    const response = await axios.post(`${API_URL}/auth/token/`, {
      username,
      password,
    });
    
    const { access, refresh } = response.data;
    setTokens(access, refresh);
    
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const logout = () => {
  clearTokens();
  // Optional: Call logout endpoint
  // api.post('/auth/logout/').catch(() => {});
};

export const register = async (userData: {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}) => {
  try {
    const response = await axios.post(`${API_URL}/auth/register/`, userData);
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// Generic data fetching function
export const fetchData = async (url: string): Promise<any> => {
  try {
    const response: AxiosResponse = await api.get(url);
    return response.data;
  } catch (error) {
    console.error(`Error fetching data from ${url}:`, error);
    throw error;
  }
};

// Page management functions
export const savePage = async (pageData: LayoutData): Promise<any> => {
  try {
    const response = await api.post('/pages/', pageData);
    return response.data;
  } catch (error) {
    console.error('Error saving page:', error);
    throw error;
  }
};

export const fetchPages = async (): Promise<any> => {
  return fetchData('/pages/');
};

export const fetchPage = async (id: string): Promise<any> => {
  return fetchData(`/pages/${id}/`);
};

export const updatePage = async (id: string, pageData: Partial<LayoutData>): Promise<any> => {
  try {
    const response = await api.patch(`/pages/${id}/`, pageData);
    return response.data;
  } catch (error) {
    console.error('Error updating page:', error);
    throw error;
  }
};

export const deletePage = async (id: string): Promise<void> => {
  try {
    await api.delete(`/pages/${id}/`);
  } catch (error) {
    console.error('Error deleting page:', error);
    throw error;
  }
};

// Initialize tokens from storage on module load
loadTokensFromStorage(); 