// Admin 会话筛选表单组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";

interface AdminConversationFilterProps {
  lang: Language;
  userId: string;
  startDate: string;
  endDate: string;
  onUserIdChange: (value: string) => void;
  onStartDateChange: (value: string) => void;
  onEndDateChange: (value: string) => void;
  onFilter: () => void;
  onReset: () => void;
}

export function AdminConversationFilter({
  lang,
  userId,
  startDate,
  endDate,
  onUserIdChange,
  onStartDateChange,
  onEndDateChange,
  onFilter,
  onReset,
}: AdminConversationFilterProps) {
  const t = adminLocales[lang];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onFilter();
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-4">
      <Input
        type="text"
        value={userId}
        onChange={(e) => onUserIdChange(e.target.value)}
        placeholder={t.userId}
        className="w-48"
      />
      <Input
        type="date"
        value={startDate}
        onChange={(e) => onStartDateChange(e.target.value)}
        className="w-40"
      />
      <Input
        type="date"
        value={endDate}
        onChange={(e) => onEndDateChange(e.target.value)}
        className="w-40"
      />
      <Button type="submit">{t.filter}</Button>
      <Button type="button" variant="outline" onClick={onReset}>
        {t.reset}
      </Button>
    </form>
  );
}
