import { useEffect, useState } from 'react';
import { askQuestion, getHistory } from '../lib/api.js';
import Chart from '../components/Chart.jsx'; // Imported from Task 9

export default function Copilot() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'error'
  const [showSql, setShowSql] = useState(false);
  const [history, setHistory] = useState([]);

  // Fetch search history immediately when the page mounts
  useEffect(() => {
    getHistory()
      .then(setHistory)
      .catch((err) => console.error("Error fetching history on mount:", err));
  }, []);

  // Central execution method for both manual form inputs and sidebar interactions
  const runQuestion = async (q) => {
    setQuestion(q);
    setStatus('loading');
    setShowSql(false);
    try {
      const data = await askQuestion(q);
      setResult(data);
      setStatus('idle');
      // Proactively refresh the sidebar with the newly stored question list
      getHistory().then(setHistory);
    } catch {
      setStatus('error');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    runQuestion(question);
  };

  return (
    <div className="max-w-5xl mx-auto p-6 flex gap-6">
      
      {/* Task 10: Query History Sidebar Layout Component */}
      <aside className="w-64 flex-none border-r border-gray-200 pr-6">
        <h2 className="text-sm font-semibold text-gray-500 mb-3 uppercase tracking-wider">History</h2>
        {history.length === 0 ? (
          <p className="text-xs text-gray-400 italic">No previous queries found.</p>
        ) : (
          <ul className="space-y-2">
            {history.map((item) => (
              <li key={item.id || item.timestamp || item.question}>
                <button
                  onClick={() => runQuestion(item.question)}
                  title={item.question}
                  className="text-left text-sm text-gray-600 hover:text-blue-600 hover:bg-gray-50 p-2 rounded block w-full truncate transition-colors"
                >
                  {item.question}
                </button>
              </li>
            ))}
          </ul>
        )}
      </aside>

      {/* Main Interactive Interface Workspace */}
      <div className="flex-1 min-w-0">
        <h1 className="text-2xl font-bold mb-4">Analytics Copilot</h1>

        <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your data…"
            className="flex-1 p-3 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-500"
            disabled={status === 'loading'}
          />
          <button
            type="submit"
            disabled={status === 'loading' || !question.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium disabled:opacity-50 hover:bg-blue-700 dynamic-btn"
          >
            {status === 'loading' ? 'Thinking…' : 'Ask'}
          </button>
        </form>

        {status === 'error' && (
          <p className="text-red-600 text-sm mb-4">Something went wrong — is the backend server running?</p>
        )}

        {/* Safety Error Notification Block */}
        {result?.error && (
          <div className="p-4 mb-4 rounded-lg bg-yellow-50 border border-yellow-200 text-sm text-yellow-800">
            The generated query didn't pass safety validation and wasn't run: {result.error}
          </div>
        )}

        {result && !result.error && (
          <div className="space-y-4">
            <p className="text-sm text-gray-700">{result.explanation}</p>

            {/* Collapsible Technical Details Action Button */}
            <div>
              <button 
                onClick={() => setShowSql((s) => !s)} 
                className="text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors focus:outline-none"
              >
                {showSql ? 'Hide SQL Query' : 'Show SQL Query'}
              </button>
              {showSql && (
                <pre className="text-xs bg-gray-50 border border-gray-200 p-3 rounded-lg mt-2 overflow-x-auto text-purple-800 font-mono">
                  {result.sql}
                </pre>
              )}
            </div>

            {/* Task 9: Dynamic Chart Context Renderer Layer */}
            {result.chart?.should_chart && (
              <div className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                <Chart result={result} />
              </div>
            )}

            {/* Task 8: Dynamic Layout Table Structure View */}
            {result.rows && result.rows.length > 0 ? (
              <div className="overflow-x-auto border border-gray-200 rounded-lg bg-white">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="border-b border-gray-200 bg-gray-50">
                      {result.columns.map((col) => (
                        <th key={col} className="text-left p-3 font-semibold text-gray-600 capitalize">
                          {col.replace(/_/g, ' ')}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.rows.map((row, i) => (
                      <tr key={i} className="border-b border-gray-100 hover:bg-gray-50/50 last:border-0">
                        {result.columns.map((col) => (
                          <td key={col} className="p-3 text-gray-700 font-mono text-xs">
                            {row[col] !== null && row[col] !== undefined ? String(row[col]) : <span className="text-gray-300">null</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-sm text-gray-400 italic">Query executed successfully but returned 0 rows.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}