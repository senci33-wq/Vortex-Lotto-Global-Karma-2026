export type GameKey = "EJ" | "L649" | "GS" | "FR";

export interface GameConfig {
  key: GameKey;
  name: string;
  short: string;
  color: string;
  mc: number; // main count
  mmin: number;
  mm: number; // main max
  ec: number; // extra count
  em: number; // extra max
  extraLabel: string | null;
  digits: boolean;
}

export const GAMES: GameConfig[] = [
  {
    key: "EJ",
    name: "Eurojackpot",
    short: "EJ",
    color: "#22d3ee",
    mc: 5,
    mmin: 1,
    mm: 50,
    ec: 2,
    em: 12,
    extraLabel: "Eurozahlen",
    digits: false,
  },
  {
    key: "L649",
    name: "Lotto 6aus49",
    short: "6aus49",
    color: "#10b981",
    mc: 6,
    mmin: 1,
    mm: 49,
    ec: 1,
    em: 9,
    extraLabel: "Superzahl",
    digits: false,
  },
  {
    key: "GS",
    name: "Glücksspirale",
    short: "Spirale",
    color: "#fbbf24",
    mc: 7,
    mmin: 0,
    mm: 9,
    ec: 0,
    em: 0,
    extraLabel: null,
    digits: true,
  },
  {
    key: "FR",
    name: "Freiheit+",
    short: "Freiheit+",
    color: "#f43f5e",
    mc: 7,
    mmin: 1,
    mm: 38,
    ec: 0,
    em: 0,
    extraLabel: null,
    digits: false,
  },
];

export const getGame = (key: GameKey): GameConfig =>
  GAMES.find((g) => g.key === key) ?? GAMES[0];
