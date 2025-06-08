import { render, screen } from "@testing-library/react";
import HomePage from "../app/page";

describe("HomePage", () => {
  it("renders welcome message", () => {
    render(<HomePage />);

    expect(screen.getByText("Welcome to MemVoice")).toBeInTheDocument();
    expect(
      screen.getByText("Memory-Optimized Voice Agent Pipeline"),
    ).toBeInTheDocument();
  });

  it("shows development environment info", () => {
    render(<HomePage />);

    expect(screen.getByText("Development Environment")).toBeInTheDocument();
    expect(
      screen.getByText("Next.js app running on port 3000"),
    ).toBeInTheDocument();
    expect(screen.getByText("FastAPI server on port 8000")).toBeInTheDocument();
  });
});
