import { http } from "@/common/http";
import type { Topic, Language } from "../types";

interface DomainConfig {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  icon: string;
  color: string;
  prompt: string;
  promptEn: string;
  isActive: boolean;
  sortOrder: number;
}

export const domainService = {
  async getActiveTopics(lang: Language): Promise<Topic[]> {
    try {
      const domains = await http.get<DomainConfig[]>("/domains/active");
      return domains.map((d) => ({
        id: d.code,
        title: lang === "zh" ? d.name : d.nameEn,
        description: lang === "zh" ? d.description : d.descriptionEn,
        icon: d.icon,
        color: d.color,
        prompt: lang === "zh" ? d.prompt : d.promptEn,
      }));
    } catch {
      return getDefaultTopics(lang);
    }
  },
};

function getDefaultTopics(lang: Language): Topic[] {
  const topics = {
    zh: [
      {
        id: "flights",
        title: "机票预订",
        description: "搜索最优惠的机票",
        icon: "Plane",
        color: "bg-blue-500",
        prompt: "我想咨询机票预订相关问题",
      },
      {
        id: "hotels",
        title: "酒店住宿",
        description: "预订舒适的住宿",
        icon: "Hotel",
        color: "bg-indigo-500",
        prompt: "我想咨询酒店住宿相关问题",
      },
      {
        id: "jobs",
        title: "求职就业",
        description: "北美求职指南",
        icon: "Briefcase",
        color: "bg-emerald-500",
        prompt: "我想咨询北美求职相关问题",
      },
      {
        id: "insurance",
        title: "保险咨询",
        description: "各类保险方案",
        icon: "ShieldCheck",
        color: "bg-cyan-500",
        prompt: "我想咨询保险相关问题",
      },
    ],
    en: [
      {
        id: "flights",
        title: "Flights",
        description: "Find the best flight deals",
        icon: "Plane",
        color: "bg-blue-500",
        prompt: "I want to inquire about flight booking",
      },
      {
        id: "hotels",
        title: "Hotels",
        description: "Book comfortable stays",
        icon: "Hotel",
        color: "bg-indigo-500",
        prompt: "I want to inquire about hotel booking",
      },
      {
        id: "jobs",
        title: "Jobs",
        description: "North America job guide",
        icon: "Briefcase",
        color: "bg-emerald-500",
        prompt: "I want to inquire about job hunting in North America",
      },
      {
        id: "insurance",
        title: "Insurance",
        description: "Insurance solutions",
        icon: "ShieldCheck",
        color: "bg-cyan-500",
        prompt: "I want to inquire about insurance",
      },
    ],
  };
  return topics[lang];
}
