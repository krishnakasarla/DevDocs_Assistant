import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import { rememberActiveChatSession } from "../chatSession";

export function useChat(initialSessionId) {
  const [sessionId, setSessionId] = useState(initialSessionId);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(Boolean(initialSessionId));
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!initialSessionId) return;
    rememberActiveChatSession(initialSessionId);
    api
      .history(initialSessionId)
      .then(({ items }) => {
        setMessages(items);
        setSessionId(initialSessionId);
      })
      .catch((reason) => setError(reason.message))
      .finally(() => setLoading(false));
  }, [initialSessionId]);

  const send = useCallback(
    async (question) => {
      const trimmed = question.trim();
      if (!trimmed || loading) return;
      setError(null);
      setMessages((current) => [
        ...current,
        { role: "user", content: trimmed, sources: [] },
      ]);
      setLoading(true);
      try {
        const result = await api.query(trimmed, sessionId);
        rememberActiveChatSession(result.session_id);
        setSessionId(result.session_id);
        setMessages((current) => [
          ...current,
          { role: "assistant", content: result.answer, sources: result.sources },
        ]);
      } catch (reason) {
        setError(reason instanceof Error ? reason.message : "Unable to get an answer");
      } finally {
        setLoading(false);
      }
    },
    [loading, sessionId],
  );

  const submit = useCallback(
    (event) => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      const question = String(form.get("question") ?? "");
      event.currentTarget.reset();
      void send(question);
    },
    [send],
  );

  return { sessionId, messages, loading, error, submit };
}
