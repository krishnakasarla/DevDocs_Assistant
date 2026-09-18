import { useLocation, useSearchParams } from "react-router-dom";
import { getActiveChatSession } from "../chatSession";
import { Citations } from "../components/Citations";
import { useChat } from "../hooks/useChat";

export function ChatPage() {
  const [params] = useSearchParams();
  const location = useLocation();
  const requestedSessionId = params.get("session") ?? undefined;
  const initialSessionId = location.state?.startNewChat
    ? undefined
    : (requestedSessionId ?? getActiveChatSession());
  const conversationKey = location.state?.startNewChat
    ? location.key
    : (initialSessionId ?? "new-chat");

  return (
    <ChatConversation
      key={conversationKey}
      initialSessionId={initialSessionId}
    />
  );
}

function ChatConversation({ initialSessionId }) {
  const { sessionId, messages, loading, error, submit } = useChat(
    initialSessionId,
  );

  return (
    <section className="chat-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Grounded documentation search</p>
          <h1>Ask about FastAPI or MongoDB</h1>
        </div>
        {sessionId && <span className="session-pill">Session {sessionId.slice(0, 8)}</span>}
      </div>

      <div className="messages" aria-live="polite">
        {!messages.length && !loading && (
          <div className="empty-state">
            <h2>Start with a concrete question</h2>
            <p>Try “How do FastAPI dependencies work?” or “When should I use a compound index?”</p>
          </div>
        )}
        {messages.map((message, index) => (
          <article className={`message ${message.role}`} key={message.id ?? index}>
            <span className="message-role">{message.role === "user" ? "You" : "Assistant"}</span>
            <p>{message.content}</p>
            <Citations sources={message.sources} />
          </article>
        ))}
        {loading && <div className="loading">Searching documentation and composing an answer…</div>}
        {error && <div className="error" role="alert">{error}</div>}
      </div>

      <form className="composer" onSubmit={submit}>
        <label className="sr-only" htmlFor="question">Question</label>
        <textarea id="question" name="question" placeholder="Ask a documentation question…" required />
        <button type="submit" disabled={loading}>{loading ? "Working…" : "Ask"}</button>
      </form>
    </section>
  );
}
