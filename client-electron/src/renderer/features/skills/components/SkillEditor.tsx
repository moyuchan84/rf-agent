import React from 'react';
import { useAgentStore } from '../../../store/useAgentStore';

const SkillEditor: React.FC = () => {
  const { skills_content, setSkillsContent } = useAgentStore();

  return (
    <div className="flex flex-col h-full bg-slate-900 text-white rounded-lg p-4 border border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Skills Editor (skills.md)</h2>
      </div>
      <textarea
        className="flex-1 bg-slate-800 border border-slate-700 rounded p-4 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        value={skills_content}
        onChange={(e) => setSkillsContent(e.target.value)}
        placeholder="### Skill: MySkill\n- Task: ...\n- Action: ..."
      />
      <div className="mt-2 text-xs text-slate-400 italic">
        Editing in Markdown format. Monaco editor integration planned.
      </div>
    </div>
  );
};

export default SkillEditor;
