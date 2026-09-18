import { NavLink, Outlet } from "react-router-dom";
import { clearActiveChatSession } from "../chatSession";

export function Layout() {
  return (
    <div className="app-shell">
      <header>
        <NavLink
          to="/"
          state={{ startNewChat: true }}
          className="brand"
          onClick={clearActiveChatSession}
        >
          DevDocs Assistant
        </NavLink>
        <nav aria-label="Main navigation">
          <NavLink to="/">Chat</NavLink>
          <NavLink to="/sessions">Sessions</NavLink>
          <NavLink to="/stats">Stats</NavLink>
        </nav>
      </header>
      <main><Outlet /></main>
    </div>
  );
}
