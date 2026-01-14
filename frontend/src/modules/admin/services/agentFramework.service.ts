// Admin Agent 框架服务
import { getApiBase, getAuthHeaders, keysToCamel } from "@/common/helper";
import type { AgentFramework, CreateAgentFrameworkDto } from "@/common/types";

const API_BASE = getApiBase();

export const agentFrameworkService = {
  async getList(): Promise<AgentFramework[]> {
    const res = await fetch(
      `${API_BASE}/data-sources?domain_code=agent_framework&limit=100`,
      { headers: getAuthHeaders() }
    );
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    return (json.data || []).map(keysToCamel) as AgentFramework[];
  },

  async refresh(id: string): Promise<void> {
    const res = await fetch(`${API_BASE}/data-sources/${id}/refresh`, {
      method: "POST",
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
  },

  async delete(id: string): Promise<void> {
    const res = await fetch(`${API_BASE}/data-sources/${id}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
  },

  async getDomains(): Promise<{ id: string; code: string }[]> {
    const res = await fetch(`${API_BASE}/data-sources/domains`, {
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    return (json.data || []).map(keysToCamel);
  },

  async getCategories(): Promise<{ id: string; code: string }[]> {
    const res = await fetch(`${API_BASE}/data-sources/categories`, {
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    return (json.data || []).map(keysToCamel);
  },

  async create(data: CreateAgentFrameworkDto): Promise<AgentFramework> {
    const domains = await this.getDomains();
    const categories = await this.getCategories();

    const agentDomain = domains.find((d) => d.code === "agent_framework");
    if (!agentDomain) throw new Error("agent_framework domain not found");

    const techCat = categories.find((c) => c.code === "tech");

    const res = await fetch(`${API_BASE}/data-sources`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: data.url,
        name: data.name || data.url.split("/").pop(),
        description: data.description,
        type: "github",
        category_id: techCat?.id,
        domain_id: agentDomain.id,
        tags: data.tags,
      }),
    });

    const json = await res.json();
    if (!json.success) throw new Error(json.message || "Failed to add");
    return keysToCamel(json.data) as AgentFramework;
  },
};
