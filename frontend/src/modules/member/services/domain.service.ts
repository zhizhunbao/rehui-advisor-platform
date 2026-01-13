// Member 领域服务 API
import { http } from "@/common/http";
import { keysToCamel } from "@/common/helper";
import type {
  Topic,
  ProductLine,
  TopicCategory,
  Lang,
  DomainConfig,
  GroupedDomain,
} from "@/common/types";

export const domainService = {
  async getProductLines(): Promise<ProductLine[]> {
    const data = await http.get<unknown[]>("/domains/product-lines");
    return keysToCamel<ProductLine[]>(data);
  },

  async getActiveTopics(lang: Lang): Promise<Topic[]> {
    const data = await http.get<unknown[]>("/domains/active");
    const domains = keysToCamel<DomainConfig[]>(data);
    return domains.map((d) => ({
      id: d.code,
      title: lang === "zh" ? d.name : d.nameEn,
      description: lang === "zh" ? d.description : d.descriptionEn,
      icon: d.icon,
      color: d.color,
      prompt: lang === "zh" ? d.prompt : d.promptEn,
      route: d.route,
    }));
  },

  async getGroupedTopics(
    lang: Lang,
    productLineId?: string
  ): Promise<TopicCategory[]> {
    const params = productLineId
      ? `?lang=${lang}&product_line_id=${productLineId}`
      : `?lang=${lang}`;
    const data = await http.get<unknown[]>(`/domains/grouped${params}`);
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
