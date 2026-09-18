export function Citations({ sources }) {
  if (!sources.length) return null;
  return (
    <details className="citations">
      <summary>{sources.length} source{sources.length === 1 ? "" : "s"}</summary>
      <ol>
        {sources.map((source) => (
          <li key={source.chunk_id}>
            <strong>{source.section_title}</strong>
            <span>{source.source_file} · similarity {source.score.toFixed(2)}</span>
          </li>
        ))}
      </ol>
    </details>
  );
}
