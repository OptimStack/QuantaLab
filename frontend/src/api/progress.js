import client from './client';

export const getMyProgress = async () => {
  const response = await client.get('/progress/me');
  return response.data;
};

export const updateProgress = async (lessonId, data) => {
  const response = await client.post(`/progress/lessons/${lessonId}`, data);
  return response.data;
};
