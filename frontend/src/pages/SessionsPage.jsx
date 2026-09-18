import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export function SessionsPage() {
  const [sessions, setSessions] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.sessions().then(setSessions).catch((reason) => setError(reason.message)).finally(() => setLoading(false));
  }, []);

  return (
    <section>
      <div className="page-heading"><div><p className="eyebrow">Conversation history</p><h1>Recent sessions</h1></div></div>
      {loading && <div className="loading">Loading sessions…</div>}
      {error && <div className="error">{error}</div>}
      {!loading && !sessions.length && <div className="empty-state"><p>No sessions yet.</p></div>}
      <div className="session-list">
        {sessions.map((session) => (
          <Link to={`/?session=${encodeURIComponent(session.session_id)}`} key={session.session_id}>
            <div><strong>{session.title}</strong><span>{new Date(session.updated_at).toLocaleString()}</span></div>
            <span>{session.message_count} messages →</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
