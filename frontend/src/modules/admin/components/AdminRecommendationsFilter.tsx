// Admin 推荐管理筛选组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface AdminRecommendationsFilterProps {
  statusFilter: string;
  onStatusFilterChange: (status: string) => void;
}

export function AdminRecommendationsFilter({
  statusFilter,
  onStatusFilterChange,
}: AdminRecommendationsFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex gap-4 mb-6">
      <Select value={statusFilter} onValueChange={onStatusFilterChange}>
        <SelectTrigger className="w-48">
          <SelectValue placeholder={t.status} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="__all__">{t.status}</SelectItem>
          <SelectItem value="PENDING">{t.pending}</SelectItem>
          <SelectItem value="APPROVED">{t.approved}</SelectItem>
          <SelectItem value="REJECTED">{t.rejected}</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
