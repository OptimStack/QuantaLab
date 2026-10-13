import client from './client';

export const login = async (email, password) => {
  const response = await client.post('/auth/login', { email, password });
  return response.data;
};

export const register = async (data) => {
  const response = await client.post('/auth/register', data);
  return response.data;
};

export const refreshToken = async () => {
  const response = await client.post('/auth/refresh');
  return response.data;
};
