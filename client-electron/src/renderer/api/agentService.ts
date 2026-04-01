import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8888',
});

export interface AgentRunResponse {
  status: string;
  message: string;
  output_file_path?: string;
  agent_logs: string[];
}

export const runAgent = async (user_query: string, skills_content: string) => {
  const response = await api.post<AgentRunResponse>('/agent/run', {
    user_query,
    skills_content,
    config: {
      model: 'ollama',
      temperature: 0.7
    }
  });
  return response.data;
};

export default api;
