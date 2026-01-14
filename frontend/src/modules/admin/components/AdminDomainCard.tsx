// Admin 领域卡片组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { Domain } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface Props {
  domain: Domain;
  categoryName: string;
  onClick: () => void;
  onToggle: () => void;
}

export function AdminDomainCard({
  domain,
  categoryName,
  onClick,
  onToggle,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const displayKeywords = (domain.discoveryKeywords || [])
    .map((kw) => {
      let clean = kw.split(" ")[0];
      if (clean.startsWith("topic:")) {
        clean = clean.replace("topic:", "");
      }
      return clean;
    })
    .filter((kw, idx, arr) => kw && arr.indexOf(kw) === idx);
  const keywordsCount = displayKeywords.length;

  return (
    <Card
      className={`cursor-pointer hover:border-primary/50 transition-all ${
        !domain.isActive ? "opacity-60" : ""
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{domain.icon}</span>
            <div>
              <h3 className="font-medium text-foreground">
                {lang === "zh" ? domain.name : domain.nameEn}
              </h3>
              <p className="text-xs text-muted-foreground font-mono">
                {domain.code}
              </p>
            </div>
          </div>
        </div>

        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {lang === "zh" ? domain.description : domain.descriptionEn}
        </p>

        {keywordsCount > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {displayKeywords.slice(0, 3).map((kw, idx) => (
              <Badge
                key={idx}
                variant="secondary"
                className="text-xs font-normal max-w-[120px] truncate"
                title={kw}
              >
                {kw}
              </Badge>
            ))}
            {keywordsCount > 3 && (
              <Badge variant="secondary" className="text-xs font-normal">
                +{keywordsCount - 3}
              </Badge>
            )}
          </div>
        )}

        <div className="flex items-center justify-between">
          <Badge variant="outline">{categoryName}</Badge>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <Badge variant={domain.isActive ? "default" : "secondary"}>
              {domain.isActive ? t.active : t.inactive}
            </Badge>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
