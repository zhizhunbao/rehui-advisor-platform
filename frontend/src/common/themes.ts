// 主题定义（shadcn 官方 + 编辑器风格主题）
export type ThemeName =
  // shadcn 官方主题
  | "zinc-light"
  | "zinc-dark"
  | "slate-light"
  | "slate-dark"
  | "stone-light"
  | "stone-dark"
  | "gray-light"
  | "gray-dark"
  | "neutral-light"
  | "neutral-dark"
  | "red-light"
  | "red-dark"
  | "rose-light"
  | "rose-dark"
  | "orange-light"
  | "orange-dark"
  | "green-light"
  | "green-dark"
  | "blue-light"
  | "blue-dark"
  | "yellow-light"
  | "yellow-dark"
  | "violet-light"
  | "violet-dark"
  // 编辑器风格主题
  | "github-light"
  | "github-dark"
  | "dracula-light"
  | "dracula-dark"
  | "nord-light"
  | "nord-dark"
  | "monokai-light"
  | "monokai-dark";

export interface Theme {
  name: ThemeName;
  label: string;
  labelEn: string;
  isDark: boolean;
  group: "shadcn" | "editor";
}

export const themes: Theme[] = [
  // shadcn 官方主题
  {
    name: "zinc-light",
    label: "Zinc 浅色",
    labelEn: "Zinc Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "zinc-dark",
    label: "Zinc 深色",
    labelEn: "Zinc Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "slate-light",
    label: "Slate 浅色",
    labelEn: "Slate Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "slate-dark",
    label: "Slate 深色",
    labelEn: "Slate Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "stone-light",
    label: "Stone 浅色",
    labelEn: "Stone Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "stone-dark",
    label: "Stone 深色",
    labelEn: "Stone Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "gray-light",
    label: "Gray 浅色",
    labelEn: "Gray Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "gray-dark",
    label: "Gray 深色",
    labelEn: "Gray Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "neutral-light",
    label: "Neutral 浅色",
    labelEn: "Neutral Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "neutral-dark",
    label: "Neutral 深色",
    labelEn: "Neutral Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "red-light",
    label: "Red 浅色",
    labelEn: "Red Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "red-dark",
    label: "Red 深色",
    labelEn: "Red Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "rose-light",
    label: "Rose 浅色",
    labelEn: "Rose Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "rose-dark",
    label: "Rose 深色",
    labelEn: "Rose Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "orange-light",
    label: "Orange 浅色",
    labelEn: "Orange Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "orange-dark",
    label: "Orange 深色",
    labelEn: "Orange Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "green-light",
    label: "Green 浅色",
    labelEn: "Green Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "green-dark",
    label: "Green 深色",
    labelEn: "Green Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "blue-light",
    label: "Blue 浅色",
    labelEn: "Blue Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "blue-dark",
    label: "Blue 深色",
    labelEn: "Blue Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "yellow-light",
    label: "Yellow 浅色",
    labelEn: "Yellow Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "yellow-dark",
    label: "Yellow 深色",
    labelEn: "Yellow Dark",
    isDark: true,
    group: "shadcn",
  },
  {
    name: "violet-light",
    label: "Violet 浅色",
    labelEn: "Violet Light",
    isDark: false,
    group: "shadcn",
  },
  {
    name: "violet-dark",
    label: "Violet 深色",
    labelEn: "Violet Dark",
    isDark: true,
    group: "shadcn",
  },
  // 编辑器风格主题
  {
    name: "github-light",
    label: "GitHub 浅色",
    labelEn: "GitHub Light",
    isDark: false,
    group: "editor",
  },
  {
    name: "github-dark",
    label: "GitHub 深色",
    labelEn: "GitHub Dark",
    isDark: true,
    group: "editor",
  },
  {
    name: "dracula-light",
    label: "Dracula 浅色",
    labelEn: "Dracula Light",
    isDark: false,
    group: "editor",
  },
  {
    name: "dracula-dark",
    label: "Dracula 深色",
    labelEn: "Dracula Dark",
    isDark: true,
    group: "editor",
  },
  {
    name: "nord-light",
    label: "Nord 浅色",
    labelEn: "Nord Light",
    isDark: false,
    group: "editor",
  },
  {
    name: "nord-dark",
    label: "Nord 深色",
    labelEn: "Nord Dark",
    isDark: true,
    group: "editor",
  },
  {
    name: "monokai-light",
    label: "Monokai 浅色",
    labelEn: "Monokai Light",
    isDark: false,
    group: "editor",
  },
  {
    name: "monokai-dark",
    label: "Monokai 深色",
    labelEn: "Monokai Dark",
    isDark: true,
    group: "editor",
  },
];

const SHADCN_THEMES = [
  "zinc",
  "slate",
  "stone",
  "gray",
  "neutral",
  "red",
  "rose",
  "orange",
  "green",
  "blue",
  "yellow",
  "violet",
];
const EDITOR_THEMES = ["github", "dracula", "nord", "monokai"];

export function applyTheme(themeName: ThemeName) {
  const root = document.documentElement;
  const theme = themes.find((t) => t.name === themeName);
  if (!theme) return;

  const parts = themeName.split("-");
  const mode = parts.pop() as "light" | "dark";
  const baseTheme = parts.join("-");

  root.classList.remove("dark");
  SHADCN_THEMES.forEach((t) => root.classList.remove(`theme-${t}`));
  EDITOR_THEMES.forEach((t) => root.classList.remove(`theme-${t}`));

  if (theme.group === "shadcn" && baseTheme !== "zinc") {
    root.classList.add(`theme-${baseTheme}`);
  } else if (theme.group === "editor") {
    root.classList.add(`theme-${baseTheme}`);
  }

  if (mode === "dark") {
    root.classList.add("dark");
  }

  localStorage.setItem("theme-name", themeName);
}

export function getStoredTheme(): ThemeName {
  return (localStorage.getItem("theme-name") as ThemeName) || "zinc-light";
}
