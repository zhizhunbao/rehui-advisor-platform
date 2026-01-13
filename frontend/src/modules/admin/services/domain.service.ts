// Admin 领域管理 API
import { http } from "@/common/http";
import type {
  Domain,
  DomainCategory,
  CreateDomainCategoryDto,
  UpdateDomainCategoryDto,
  CreateDomainDto,
  UpdateDomainDto,
} from "@/common/types";

export const domainCategoryService = {
  getAll() {
    return http.get<DomainCategory[]>("/admin/domain-categories");
  },
  getById(id: string) {
    return http.get<DomainCategory>(`/admin/domain-categories/${id}`);
  },
  create(data: CreateDomainCategoryDto) {
    return http.post<DomainCategory>("/admin/domain-categories", data);
  },
  update(id: string, data: UpdateDomainCategoryDto) {
    return http.put<DomainCategory>(`/admin/domain-categories/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/domain-categories/${id}`);
  },
};

export const domainService = {
  getAll(categoryId?: string) {
    const query = categoryId ? `?category_id=${categoryId}` : "";
    return http.get<Domain[]>(`/admin/domains${query}`);
  },
  getById(id: string) {
    return http.get<Domain>(`/admin/domains/${id}`);
  },
  create(data: CreateDomainDto) {
    return http.post<Domain>("/admin/domains", data);
  },
  update(id: string, data: UpdateDomainDto) {
    return http.put<Domain>(`/admin/domains/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/domains/${id}`);
  },
};
