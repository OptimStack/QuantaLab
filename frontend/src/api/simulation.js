import client from './client';

export const submitSimulation = async (circuitId, backend, shots) => {
  const response = await client.post('/simulate', { circuitId, backend, shots });
  return response.data;
};

export const getJobStatus = async (jobId) => {
  const response = await client.get(`/simulate/jobs/${jobId}`);
  return response.data;
};

export const subscribeToJob = (jobId, onUpdate) => {
  const wsUrl = (import.meta.env.VITE_WS_BASE_URL || '/ws') + `/jobs/${jobId}`;
  const ws = new WebSocket(wsUrl);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onUpdate(data);
  };
  
  return ws;
};
