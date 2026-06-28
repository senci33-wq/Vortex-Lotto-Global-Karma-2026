import { GameKey } from "@/src/data/games";

const BASE = `${process.env.EXPO_PUBLIC_BACKEND_URL}/api`;

export interface DrawResult {
  game: string;
  name: string;
  main: number[];
  extra: number[];
  source: "quantum" | "crypto";
  extraLabel: string | null;
  generated_at: string;
}

export interface ProjectItem {
  name: string;
  url: string;
}
export interface CategoryGroup {
  category: string;
  count: number;
  projects: ProjectItem[];
}
export interface ProjectsResponse {
  categories: CategoryGroup[];
  total: number;
}

export interface Draw {
  id: string;
  game: string;
  main: number[];
  extra: number[];
  created_at: string;
}

export interface AnalysisResult {
  game: string;
  name: string;
  totalDraws: number;
  max: number;
  counts: { n: number; count: number }[];
  hot: { n: number; count: number }[];
  cold: { n: number; count: number }[];
}

async function req<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const j = await res.json();
      detail = j.detail || detail;
    } catch {}
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export const api = {
  drawQuantum: (game: GameKey) =>
    req<DrawResult>("/quantum/draw", {
      method: "POST",
      body: JSON.stringify({ game }),
    }),
  getProjects: () => req<ProjectsResponse>("/projects"),
  listDraws: (game: GameKey) => req<Draw[]>(`/draws?game=${game}`),
  addDraw: (game: GameKey, main: number[], extra: number[]) =>
    req<Draw>("/draws", {
      method: "POST",
      body: JSON.stringify({ game, main, extra }),
    }),
  deleteDraw: (id: string) => req(`/draws/${id}`, { method: "DELETE" }),
  getAnalysis: (game: GameKey) => req<AnalysisResult>(`/analysis?game=${game}`),
};
