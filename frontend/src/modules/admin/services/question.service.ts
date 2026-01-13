// Admin 问题库管理 API
import { http } from "@/common/http";
import type { Question, CreateQuestionDto } from "@/common/types";

export const questionService = {
  getAll(domainId?: string) {
    const query = domainId ? `?domainId=${domainId}` : "";
    return http.get<Question[]>(`/admin/questions${query}`);
  },
  getById(id: string) {
    return http.get<Question>(`/admin/questions/${id}`);
  },
  create(data: CreateQuestionDto) {
    return http.post<Question>("/admin/questions", data);
  },
  update(id: string, data: Partial<CreateQuestionDto>) {
    return http.put<Question>(`/admin/questions/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/questions/${id}`);
  },
};
