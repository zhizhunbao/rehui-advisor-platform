// Member 首页服务 API
import { http } from "@/common/http";
import { keysToCamel } from "@/common/helper";
import type { TopicCategory, Lang, GroupedDomain } from "@/common/types";

export const homeService = {
  async getGroupedTopics(lang: Lang): Promise<TopicCategory[]> {
    const data = await http.get<unknown[]>(`/domains/grouped?lang=${lang}`);
    const grouped = keysToCamel<GroupedDomain[]>(data);
    return grouped.map((g) => ({
      id: g.id,
      code: g.code,
      name: g.name,
      icon: g.icon,
      color: g.color,
      topics: g.domains.map((d) => ({
        id: d.code || d.id,
        title: lang === "zh" ? d.name : d.nameEn,
        description: lang === "zh" ? d.description : d.descriptionEn,
        icon: d.icon,
        color: d.color,
        prompt: lang === "zh" ? d.prompt : d.promptEn,
        route: d.route,
      })),
    }));
  },
};
