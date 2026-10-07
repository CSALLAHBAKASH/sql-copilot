const BASE_URL = import.meta.env.VITE_API_URL;

export async function askQuestion(question) {
  const res = await fetch(`${BASE_URL}/api/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${BASE_URL}/api/history`);
  if (!res.ok) throw new Error('Failed to load history');
  return res.json();
}