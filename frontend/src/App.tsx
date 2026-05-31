import React, { useState } from 'react';

function App() {
  const [prompt, setPrompt] = useState('');
  const [jobId, setJobId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/v1/goals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      const data = await response.json();
      setJobId(data.job_id);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4">
      <header className="max-w-3xl w-full flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Gemini Cowork</h1>
        <div className="text-sm font-medium text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
          Autonomous OS
        </div>
      </header>
      
      <main className="max-w-3xl w-full bg-white shadow-xl rounded-2xl overflow-hidden flex flex-col border border-gray-100">
        
        {/* Goal Input */}
        <div className="p-6 border-b border-gray-100 bg-gray-50/50">
          <form onSubmit={handleSubmit} className="relative">
            <textarea
              className="w-full bg-white border border-gray-200 rounded-xl p-4 pr-24 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              rows={3}
              placeholder="E.g., Analyze the Q3 financial PDFs and generate a board presentation..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <button
              type="submit"
              className="absolute bottom-4 right-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow transition-colors"
            >
              Execute
            </button>
          </form>
        </div>

        {/* Execution State */}
        <div className="p-6 min-h-[400px]">
          {jobId ? (
            <div className="flex flex-col space-y-4">
              <div className="flex items-center space-x-3 text-sm text-gray-600">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-600 border-t-transparent"></div>
                <span>Orchestrator generating execution DAG for Job: {jobId}...</span>
              </div>
              {/* Future: Render live DAG visualization here */}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              Awaiting high-level goal submission.
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
