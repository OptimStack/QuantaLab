import client from './client';

export const getAssessment = async (id) => {
  const response = await client.get(`/assessments/${id}`);
  return response.data;
};

export const submitAssessment = async (id, answers) => {
  const response = await client.post(`/assessments/${id}/submit`, { answers });
  return response.data;
};

export const getAssessmentsByLesson = async (lessonId) => {
  const response = await client.get(`/assessments?lessonId=${lessonId}`);
  return response.data;
};
