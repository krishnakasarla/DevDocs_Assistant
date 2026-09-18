const ACTIVE_CHAT_SESSION_KEY = "devdocs.activeChatSession";

export function getActiveChatSession() {
  try {
    return window.sessionStorage.getItem(ACTIVE_CHAT_SESSION_KEY) ?? undefined;
  } catch {
    return undefined;
  }
}

export function rememberActiveChatSession(sessionId) {
  try {
    window.sessionStorage.setItem(ACTIVE_CHAT_SESSION_KEY, sessionId);
  } catch {
    // The chat still works if browser storage is unavailable.
  }
}

export function clearActiveChatSession() {
  try {
    window.sessionStorage.removeItem(ACTIVE_CHAT_SESSION_KEY);
  } catch {
    // The navigation itself still starts a fresh in-memory chat.
  }
}
