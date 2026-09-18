import { lazy, Suspense } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Layout } from "./components/Layout";

const ChatPage = lazy(() =>
  import("./pages/ChatPage").then((module) => ({ default: module.ChatPage })),
);
const SessionsPage = lazy(() =>
  import("./pages/SessionsPage").then((module) => ({ default: module.SessionsPage })),
);
const StatsPage = lazy(() =>
  import("./pages/StatsPage").then((module) => ({ default: module.StatsPage })),
);

function pending(element) {
  return <Suspense fallback={<div className="loading">Loading page…</div>}>{element}</Suspense>;
}

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: pending(<ChatPage />) },
      { path: "/sessions", element: pending(<SessionsPage />) },
      { path: "/stats", element: pending(<StatsPage />) },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}
