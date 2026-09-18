const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const problem = await response.json().catch(() => null);
    throw new Error(problem?.detail ?? `Request failed (${response.status})`);
  }
  return response.json();
}

export const api = {
  query: (question, sessionId) =>
    request(
      "/api/v1/query",
      { method: "POST", body: JSON.stringify({ question, session_id: sessionId }) },
    ),
  sessions: () => request("/api/v1/sessions"),
  history: (sessionId) =>
    request(
      `/api/v1/sessions/${encodeURIComponent(sessionId)}/history?page_size=100`,
    ),
  stats: () => request("/api/v1/stats"),
};
