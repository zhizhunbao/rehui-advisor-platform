import { http } from "@/common/http";
import type {
  SubscriptionPlan,
  CreateSubscriptionDto,
  UpdateSubscriptionDto,
} from "@/common/types";

export const subscriptionService = {
  getAll() {
    return http.get<SubscriptionPlan[]>("/admin/subscriptions");
  },

  getById(id: string) {
    return http.get<SubscriptionPlan>(`/admin/subscriptions/${id}`);
  },

  create(data: CreateSubscriptionDto) {
    return http.post<SubscriptionPlan>("/admin/subscriptions", data);
  },

  update(id: string, data: UpdateSubscriptionDto) {
    return http.put<SubscriptionPlan>(`/admin/subscriptions/${id}`, data);
  },

  delete(id: string) {
    return http.delete<void>(`/admin/subscriptions/${id}`);
  },
};
