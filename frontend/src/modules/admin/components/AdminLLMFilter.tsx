// Admin LLM 筛选组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminTagFilter } from "./AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";

interface FilterOption {
  value: string;
  label: string;
  count: number;
}

interface AdminLLMFilterProps {
  searchQuery: string;
  filterProvider: string;
  filterCategory: string;
  filterDeployment: string;
  filterInputPrice: string;
  filterOutputPrice: string;
  filterContext: string;
  providerCounts: FilterOption[];
  categoryCounts: FilterOption[];
  deploymentCounts: FilterOption[];
  inputPriceCounts: FilterOption[];
  outputPriceCounts: FilterOption[];
  contextCounts: FilterOption[];
  hasFilters: boolean;
  onSearchChange: (value: string) => void;
  onProviderChange: (value: string) => void;
  onCategoryChange: (value: string) => void;
  onDeploymentChange: (value: string) => void;
  onInputPriceChange: (value: string) => void;
  onOutputPriceChange: (value: string) => void;
  onContextChange: (value: string) => void;
  onReset: () => void;
}

export function AdminLLMFilter({
  searchQuery,
  filterProvider,
  filterCategory,
  filterDeployment,
  filterInputPrice,
  filterOutputPrice,
  filterContext,
  providerCounts,
  categoryCounts,
  deploymentCounts,
  inputPriceCounts,
  outputPriceCounts,
  contextCounts,
  hasFilters,
  onSearchChange,
  onProviderChange,
  onCategoryChange,
  onDeploymentChange,
  onInputPriceChange,
  onOutputPriceChange,
  onContextChange,
  onReset,
}: AdminLLMFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="space-y-4">
      {providerCounts.length > 0 && (
        <AdminTagFilter
          label={t.company}
          options={providerCounts}
          value={filterProvider || "__all__"}
          onChange={(v) => onProviderChange(v === "__all__" ? "" : v)}
          color="violet"
        />
      )}

      {categoryCounts.length > 0 && (
        <AdminTagFilter
          label={t.category}
          options={categoryCounts}
          value={filterCategory || "__all__"}
          onChange={(v) => onCategoryChange(v === "__all__" ? "" : v)}
          color="blue"
        />
      )}

      {deploymentCounts.length > 0 && (
        <AdminTagFilter
          label={t.deploymentType}
          options={deploymentCounts}
          value={filterDeployment || "__all__"}
          onChange={(v) => onDeploymentChange(v === "__all__" ? "" : v)}
          color="emerald"
        />
      )}

      {inputPriceCounts.length > 0 && (
        <AdminTagFilter
          label={t.inputPrice}
          options={inputPriceCounts}
          value={filterInputPrice || "__all__"}
          onChange={(v) => onInputPriceChange(v === "__all__" ? "" : v)}
          color="amber"
        />
      )}

      {outputPriceCounts.length > 0 && (
        <AdminTagFilter
          label={t.outputPrice}
          options={outputPriceCounts}
          value={filterOutputPrice || "__all__"}
          onChange={(v) => onOutputPriceChange(v === "__all__" ? "" : v)}
          color="orange"
        />
      )}

      {contextCounts.length > 0 && (
        <AdminTagFilter
          label={t.context}
          options={contextCounts}
          value={filterContext || "__all__"}
          onChange={(v) => onContextChange(v === "__all__" ? "" : v)}
          color="rose"
        />
      )}

      <div className="flex gap-4 items-center">
        <Input
          placeholder={t.searchModels}
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-[200px]"
        />
        {hasFilters && (
          <Button variant="outline" size="sm" onClick={onReset}>
            {t.reset}
          </Button>
        )}
      </div>
    </div>
  );
}
