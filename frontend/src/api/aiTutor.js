import client from './client';

export const createTutorSession = async (lessonId, circuitId) => {
  const response = await client.post('/tutor/session', { lessonId, circuitId });
  return response.data;
};
