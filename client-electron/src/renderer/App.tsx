import React from 'react';
import SkillEditor from './features/skills/components/SkillEditor';
import { useAgentStore } from './store/useAgentStore';
import { runAgent } from './api/agentService';
import { Terminal, Send, Play, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const App: React.FC = () => {
  const { 
    user_query, 
    setUserQuery, 
    skills_content, 
    agent_response, 
    setAgentResponse, 
    isLoading, 
    setIsLoading 
  } = useAgentStore();

  const handleRun = async () => {
    if (!user_query.trim() || !skills_content.trim()) return;
    
    setIsLoading(true);
    setAgentResponse(null);
    try {
      const result = await runAgent(user_query, skills_content);
      setAgentResponse(result);
    } catch (error) {
      console.error(error);
      setAgentResponse({
        status: 'error',
        message: 'Failed to run agent. Check connection to FastAPI.',
        agent_logs: ['Error: ' + (error as any).message]
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Sidebar - Skills Editor */}
      <aside className="w-1/3 border-r border-slate-800 p-4">
        <SkillEditor />
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col p-6">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <Terminal className="text-blue-500" />
            Agent Gateway
          </h1>
          <p className="text-slate-400">Interact with your MAS-powered Agent</p>
        </header>

        {/* Query Input */}
        <section className="mb-6 flex gap-3">
          <input
            className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg transition-all"
            value={user_query}
            onChange={(e) => setUserQuery(e.target.value)}
            placeholder="Ask your agent anything..."
            disabled={isLoading}
            onKeyDown={(e) => e.key === 'Enter' && handleRun()}
          />
          <button
            className={`px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-all ${
              isLoading 
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-500 active:scale-95 text-white'
            }`}
            onClick={handleRun}
            disabled={isLoading}
          >
            {isLoading ? <Clock className="animate-spin" size={20} /> : <Play size={20} />}
            Run Agent
          </button>
        </section>

        {/* Output/Logs */}
        <section className="flex-1 flex flex-col min-h-0 bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden backdrop-blur-sm">
          <div className="bg-slate-800/50 px-4 py-2 border-b border-slate-800 flex justify-between items-center">
            <span className="text-sm font-medium uppercase tracking-wider text-slate-400">Logs & Response</span>
            {agent_response?.status === 'success' && <CheckCircle className="w-4 h-4 text-green-500" />}
            {agent_response?.status === 'error' && <AlertCircle className="w-4 h-4 text-red-500" />}
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 font-mono text-sm space-y-4 custom-scrollbar">
            {!agent_response && !isLoading && (
              <div className="h-full flex flex-col items-center justify-center text-slate-500 opacity-50">
                <Send size={48} className="mb-4" />
                <p>Run the agent to see logs and results here.</p>
              </div>
            )}

            {isLoading && (
              <div className="flex items-center gap-3 text-blue-400">
                <Clock className="animate-spin w-4 h-4" />
                <span>Agent is working...</span>
              </div>
            )}

            {agent_response && (
              <>
                <div className="p-4 rounded-lg bg-slate-800/80 border border-slate-700">
                  <div className={`font-bold mb-1 ${agent_response.status === 'success' ? 'text-green-400' : 'text-red-400'}`}>
                    {agent_response.status.toUpperCase()}
                  </div>
                  <p>{agent_response.message}</p>
                  {agent_response.output_file_path && (
                    <div className="mt-3 p-2 bg-slate-950 rounded text-xs border border-slate-800 flex items-center gap-2">
                      <span className="text-slate-500">Output:</span>
                      <span className="text-blue-300 truncate">{agent_response.output_file_path}</span>
                    </div>
                  )}
                </div>

                <div className="space-y-1">
                  {agent_response.agent_logs.map((log, idx) => (
                    <div key={idx} className="flex gap-3">
                      <span className="text-slate-600 w-4 select-none">{idx + 1}</span>
                      <span className="text-slate-300">{log}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </section>
      </main>
    </div>
  );
};

export default App;
