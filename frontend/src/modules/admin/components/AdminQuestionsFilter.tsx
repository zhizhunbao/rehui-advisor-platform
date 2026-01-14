// Admin 问题管理筛选组件
import type { Domain } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface AdminQuestionsFilterProps {
  domains: Domain[];
  selectedDomainId: string;
  onDomainChange: (id: string) => void;
}

export function AdminQuestionsFilter({
  domains,
  selectedDomainId,
  onDomainChange,
}: AdminQuestionsFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="mb-6">
      <Select value={selectedDomainId} onValueChange={onDomainChange}>
        <SelectTrigger className="w-48">
          <SelectValue placeholder={t.allDomains} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">{t.allDomains}</SelectItem>
          {domains.map((d) => (
            <SelectItem key={d.id} value={d.id}>
              {lang === "zh" ? d.name : d.nameEn}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
