// Admin 领域列表组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { Domain, DomainCategory } from "@/common/types";
import { Card, CardContent } from "@/libs/shadcn/ui/card";
import { AdminDomainCard } from "./AdminDomainCard";

interface Props {
  isGroupedMode: boolean;
  filteredDomains: Domain[];
  groupedDomains: { category: DomainCategory; domains: Domain[] }[];
  isLoading: boolean;
  getCategoryName: (categoryId: string) => string;
  onSelect: (domain: Domain) => void;
  onToggle: (domain: Domain) => void;
}

export function AdminDomainsList({
  isGroupedMode,
  filteredDomains,
  groupedDomains,
  isLoading,
  getCategoryName,
  onSelect,
  onToggle,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  if (isGroupedMode) {
    if (groupedDomains.length === 0) {
      return (
        <div className="text-center text-muted-foreground py-12">
          {t.noData}
        </div>
      );
    }

    return (
      <div className="space-y-8">
        {groupedDomains.map(({ category, domains }) => (
          <Card key={category.id}>
            <CardContent className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">{category.icon}</span>
                <h2 className="text-xl font-bold text-foreground">
                  {lang === "zh" ? category.name : category.nameEn}{" "}
                  <span className="text-sm font-normal text-muted-foreground">
                    ({domains.length})
                  </span>
                </h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {domains.map((domain) => (
                  <AdminDomainCard
                    key={domain.id}
                    domain={domain}
                    categoryName={getCategoryName(domain.categoryId)}
                    onClick={() => onSelect(domain)}
                    onToggle={() => onToggle(domain)}
                  />
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (filteredDomains.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-12">{t.noData}</div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {filteredDomains.map((domain) => (
        <AdminDomainCard
          key={domain.id}
          domain={domain}
          categoryName={getCategoryName(domain.categoryId)}
          onClick={() => onSelect(domain)}
          onToggle={() => onToggle(domain)}
        />
      ))}
    </div>
  );
}
