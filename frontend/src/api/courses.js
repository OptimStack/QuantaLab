import client from './client';

export const getCourses = async () => {
  const response = await client.get('/courses');
  return response.data;
};

export const getCourse = async (id) => {
  const response = await client.get(`/courses/${id}`);
  return response.data;
};

export const getLesson = async (id) => {
  const response = await client.get(`/lessons/${id}`);
  return response.data;
};
