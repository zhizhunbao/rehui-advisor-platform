// 国际化入口 - 集中管理
import zh from "./i18n/zh";
import en from "./i18n/en";

export type Language = "zh" | "en";

// 完整翻译对象
export const locales = { zh, en };

// Hook - 获取当前语言的翻译
export function useI18n(lang: Language) {
  return locales[lang];
}

// 快捷访问 - 兼容旧代码
export const common = {
  zh: zh.common,
  en: en.common,
};

export const adminLocales = {
  zh: { ...zh.common, ...zh.admin },
  en: { ...en.common, ...en.admin },
};

export const advisorLocales = {
  zh: { ...zh.common, ...zh.advisor },
  en: { ...en.common, ...en.advisor },
};

export const authLocales = {
  zh: { ...zh.common, ...zh.auth },
  en: { ...en.common, ...en.auth },
};
