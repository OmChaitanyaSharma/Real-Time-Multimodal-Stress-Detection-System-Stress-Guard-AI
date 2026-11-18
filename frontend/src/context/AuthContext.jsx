import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('stress_auth_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('stress_auth_token');
      if (storedToken) {
        try {
          const res = await authAPI.getProfile();
          setUser(res.data);
        } catch (err) {
          console.error('Session expired or invalid:', err);
          logout();
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login(email, password);
    const accessToken = res.data.access_token;
    localStorage.setItem('stress_auth_token', accessToken);
    setToken(accessToken);
    const profileRes = await authAPI.getProfile();
    setUser(profileRes.data);
    localStorage.setItem('stress_auth_user', JSON.stringify(profileRes.data));
    return profileRes.data;
  };

  const register = async (fullName, email, password) => {
    await authAPI.register(fullName, email, password);
    return login(email, password);
  };

  const logout = () => {
    localStorage.removeItem('stress_auth_token');
    localStorage.removeItem('stress_auth_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
