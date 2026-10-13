import client from './client';

export const getCircuits = async () => {
  const response = await client.get('/circuits');
  return response.data;
};

export const getCircuit = async (id) => {
  const response = await client.get(`/circuits/${id}`);
  return response.data;
};

export const saveCircuit = async (data) => {
  const response = await client.post('/circuits', data);
  return response.data;
};

export const updateCircuit = async (id, data) => {
  const response = await client.put(`/circuits/${id}`, data);
  return response.data;
};

export const exportQasm = async (id) => {
  const response = await client.get(`/circuits/${id}/qasm`);
  return response.data;
};

export const importQasm = async (id, qasmStr) => {
  const response = await client.post(`/circuits/${id}/import`, { qasm: qasmStr });
  return response.data;
};
