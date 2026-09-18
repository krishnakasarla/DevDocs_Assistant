import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Citations } from "./Citations";

describe("Citations", () => {
  it("renders source attribution", () => {
    render(<Citations sources={[{ chunk_id: "1", source_file: "fastapi/body.md", section_title: "Body", doc_type: "fastapi", chunk_text: "text", score: 0.9 }]} />);
    expect(screen.getByText("Body")).toBeInTheDocument();
    expect(screen.getByText(/fastapi\/body.md/)).toBeInTheDocument();
  });
});
