import { create } from 'zustand';

export interface AgentResponse {
  status: string;
  message: string;
  output_file_path?: string;
  agent_logs: string[];
}

interface AgentState {
  user_query: string;
  skills_content: string;
  agent_response: AgentResponse | null;
  isLoading: boolean;
  setUserQuery: (query: string) => void;
  setSkillsContent: (content: string) => void;
  setAgentResponse: (response: AgentResponse | null) => void;
  setIsLoading: (loading: boolean) => void;
}

export const useAgentStore = create<AgentState>((set) => ({
  user_query: '',
  skills_content: '### Skill: Example\n- Task: Write a short greeting\n- Action: Print hello',
  agent_response: null,
  isLoading: false,
  setUserQuery: (user_query) => set({ user_query }),
  setSkillsContent: (skills_content) => set({ skills_content }),
  setAgentResponse: (agent_response) => set({ agent_response }),
  setIsLoading: (isLoading) => set({ isLoading }),
}));
