const SECTION_LABEL_LIMIT = 24;

export function normalizeSectionLabel(value) {
  return String(value).replace(/\s+/g, " ").trim();
}

export function formatSectionLabel(value) {
  const label = normalizeSectionLabel(value);
  if (label.length <= SECTION_LABEL_LIMIT) return label;
  return `${label.slice(0, SECTION_LABEL_LIMIT - 1).trimEnd()}…`;
}
