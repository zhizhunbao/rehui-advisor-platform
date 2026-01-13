// Admin 会话管理 API
import { http } from "@/common/http";
import type {
  AdminConversation,
  PaginatedResponse,
  ConversationListParams,
} from "@/common/types";

export const conversationService = {
  getAll(params?: ConversationListParams) {
    const query = new URLSearchParams();
    if (params?.page) query.set("page", String(params.page));
    if (params?.limit) query.set("limit", String(params.limit));
    if (params?.userId) query.set("user_id", params.userId);
    if (params?.startDate) query.set("start_date", params.startDate);
    if (params?.endDate) query.set("end_date", params.endDate);
    const queryStr = query.toString();
    return http.get<PaginatedResponse<AdminConversation>>(
      `/admin/conversations${queryStr ? `?${queryStr}` : ""}`
    );
  },

  getById(id: string) {
    return http.get<AdminConversation>(`/admin/conversations/${id}`);
  },

  delete(id: string) {
    return http.delete<void>(`/admin/conversations/${id}`);
  },
};
