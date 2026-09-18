import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { api } from "../api/client";
import { formatSectionLabel, normalizeSectionLabel } from "./statsFormat";

function SectionAxisTick({ x = 0, y = 0, payload = {} }) {
  return (
    <text
      x={x}
      y={y}
      dy="0.32em"
      fill="#666"
      fontSize={12}
      textAnchor="end"
    >
      {formatSectionLabel(payload.value ?? "")}
    </text>
  );
}

export function StatsPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.stats().then(setStats).catch((reason) => setError(reason.message));
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (!stats) return <div className="loading">Loading analytics…</div>;

  const citedSectionsChartHeight = Math.max(
    280,
    stats.most_queried_sections.length * 38,
  );

  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Retrieval analytics</p>
          <h1>Usage stats</h1>
        </div>
      </div>
      <div className="metric">
        <span>Average sources per answer</span>
        <strong>{stats.average_sources_per_answer.toFixed(1)}</strong>
      </div>
      <div className="chart-grid">
        <article className="chart-card">
          <h2>Queries over time</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={stats.query_volume_over_time}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#5b5bd6" />
            </BarChart>
          </ResponsiveContainer>
        </article>
        <article className="chart-card">
          <h2>Most cited sections</h2>
          <ResponsiveContainer width="100%" height={citedSectionsChartHeight}>
            <BarChart
              data={stats.most_queried_sections}
              layout="vertical"
              margin={{ top: 4, right: 12, bottom: 4, left: 4 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" allowDecimals={false} />
              <YAxis
                type="category"
                dataKey="section_title"
                width={150}
                interval={0}
                tick={<SectionAxisTick />}
              />
              <Tooltip
                formatter={(value) => [value, "Citations"]}
                labelFormatter={normalizeSectionLabel}
              />
              <Bar dataKey="count" fill="#14a38b" />
            </BarChart>
          </ResponsiveContainer>
        </article>
      </div>
    </section>
  );
}
