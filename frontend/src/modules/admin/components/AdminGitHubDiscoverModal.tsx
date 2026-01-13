// Admin GitHub 发现弹窗组件 - Props: lang, categories, domainKeywords, results, onClose, onSearch, onImport
import { useState } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Checkbox } from "@/libs/shadcn/ui/checkbox";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/libs/shadcn/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

export interface GitHubRepo {
  url: string;
  name: string;
  fullName: string;
  description: string;
  stars: number;
  forks: number;
  language: string;
  topics: string[];
  updatedAt: string;
  owner: string;
  repo: string;
  alreadyExists: boolean;
}

export interface DomainKeywords {
  domain: string;
  nameZh: string;
  nameEn: string;
  keywords: string[];
}

export interface Category {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

export interface Domain {
  id: string;
  code: string;
  name: string;
  nameEn: string;
}

interface AdminGitHubDiscoverModalProps {
  lang: Language;
  categories: Category[];
  domainKeywords: DomainKeywords[];
  domains: Domain[];
  results: GitHubRepo[];
  isSearching: boolean;
  isAutoDiscovering: boolean;
  isImporting: boolean;
  error: string;
  onClose: () => void;
  onSearch: (query: string, sort: string, perPage: number) => void;
  onAutoDiscover: (domain: string) => void;
  onImport: (items: GitHubRepo[], categoryId: string, domainId: string) => void;
  onCategoryChange: (categoryId: string) => void;
}

export function AdminGitHubDiscoverModal({
  lang,
  categories,
  domainKeywords,
  domains,
  results,
  isSearching,
  isAutoDiscovering,
  isImporting,
  error,
  onClose,
  onSearch,
  onAutoDiscover,
  onImport,
  onCategoryChange,
}: AdminGitHubDiscoverModalProps) {
  const t = adminLocales[lang];

  const [activeTab, setActiveTab] = useState("manual");
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("stars");
  const [perPage, setPerPage] = useState("30");
  const [categoryId, setCategoryId] = useState("");
  const [domainId, setDomainId] = useState("");
  const [selectedDomain, setSelectedDomain] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const handleSearch = () => {
    if (!query.trim()) return;
    setSelected(new Set());
    onSearch(query.trim(), sort, parseInt(perPage));
  };

  const handleAutoDiscover = () => {
    if (!selectedDomain) return;
    setSelected(new Set());
    onAutoDiscover(selectedDomain);
    if (!categoryId) setCategoryId(selectedDomain);
  };

  const handleToggleSelect = (url: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(url)) next.delete(url);
      else next.add(url);
      return next;
    });
  };

  const selectableCount = results.filter((r) => !r.alreadyExists).length;

  const handleSelectAll = () => {
    const selectable = results.filter((r) => !r.alreadyExists);
    if (selected.size === selectable.length) setSelected(new Set());
    else setSelected(new Set(selectable.map((r) => r.url)));
  };

  const handleImport = () => {
    if (selected.size === 0 || !categoryId) return;
    const items = results.filter((r) => selected.has(r.url));
    onImport(items, categoryId, domainId);
  };

  const handleCategoryChange = (value: string) => {
    setCategoryId(value);
    setDomainId("");
    onCategoryChange(value);
  };

  return (
    <Dialog open={true} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle>{t.discoverGithub}</DialogTitle>
        </DialogHeader>

        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="flex-1 flex flex-col overflow-hidden"
        >
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="manual">{t.search}</TabsTrigger>
            <TabsTrigger value="auto">{t.autoDiscover}</TabsTrigger>
          </TabsList>

          <TabsContent value="manual" className="space-y-4 mt-4">
            <div className="flex gap-2 items-end flex-wrap">
              <div className="flex-1 min-w-[200px]">
                <label className="text-sm text-muted-foreground mb-1 block">
                  {t.searchQuery}
                </label>
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g. machine learning, react hooks"
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                />
              </div>
              <div className="w-32">
                <label className="text-sm text-muted-foreground mb-1 block">
                  {t.sortBy}
                </label>
                <Select value={sort} onValueChange={setSort}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="stars">{t.sortStars}</SelectItem>
                    <SelectItem value="updated">{t.sortUpdated}</SelectItem>
                    <SelectItem value="forks">{t.sortForks}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="w-24">
                <label className="text-sm text-muted-foreground mb-1 block">
                  {t.perPage}
                </label>
                <Select value={perPage} onValueChange={setPerPage}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="10">10</SelectItem>
                    <SelectItem value="30">30</SelectItem>
                    <SelectItem value="50">50</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button
                onClick={handleSearch}
                disabled={isSearching || !query.trim()}
              >
                {isSearching ? t.searching : t.search}
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="auto" className="space-y-4 mt-4">
            <div className="flex gap-4 items-end">
              <div className="flex-1">
                <label className="text-sm text-muted-foreground mb-1 block">
                  {t.selectDomain}
                </label>
                <Select
                  value={selectedDomain}
                  onValueChange={setSelectedDomain}
                >
                  <SelectTrigger>
                    <SelectValue placeholder={t.selectDomain} />
                  </SelectTrigger>
                  <SelectContent>
                    {domainKeywords.map((d) => (
                      <SelectItem key={d.domain} value={d.domain}>
                        {lang === "zh" ? d.nameZh : d.nameEn} (
                        {d.keywords.length} {t.keywords})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <Button
                onClick={handleAutoDiscover}
                disabled={isAutoDiscovering || !selectedDomain}
              >
                {isAutoDiscovering ? t.discovering : t.startDiscover}
              </Button>
            </div>
            {selectedDomain && (
              <div className="text-sm text-muted-foreground">
                {t.keywords}:{" "}
                {domainKeywords
                  .find((d) => d.domain === selectedDomain)
                  ?.keywords.join(", ")}
              </div>
            )}
          </TabsContent>
        </Tabs>

        <div className="space-y-4 flex-1 overflow-hidden flex flex-col">
          <div className="flex gap-4">
            <div className="w-48">
              <label className="text-sm text-muted-foreground mb-1 block">
                {t.category} *
              </label>
              <Select value={categoryId} onValueChange={handleCategoryChange}>
                <SelectTrigger>
                  <SelectValue placeholder={t.selectCategory} />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((c) => (
                    <SelectItem key={c.id} value={c.id}>
                      {lang === "zh" ? c.name : c.nameEn || c.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="w-48">
              <label className="text-sm text-muted-foreground mb-1 block">
                {t.domain}
              </label>
              <Select
                value={domainId}
                onValueChange={setDomainId}
                disabled={!categoryId || domains.length === 0}
              >
                <SelectTrigger>
                  <SelectValue placeholder="-" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">-</SelectItem>
                  {domains.map((d) => (
                    <SelectItem key={d.id} value={d.id}>
                      {lang === "zh" ? d.name : d.nameEn || d.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {error && <div className="text-sm text-destructive">{error}</div>}

          {results.length > 0 && (
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">
                {t.searchResults}: {results.length} | {t.selected}:{" "}
                {selected.size}
              </div>
              <Button variant="outline" size="sm" onClick={handleSelectAll}>
                {selected.size === selectableCount
                  ? t.deselectAll
                  : t.selectAll}
              </Button>
            </div>
          )}

          <div className="flex-1 overflow-y-auto space-y-2 max-h-[300px]">
            {results.map((repo) => (
              <div
                key={repo.url}
                className={`p-3 border rounded-lg flex items-start gap-3 ${
                  repo.alreadyExists
                    ? "opacity-50 bg-muted"
                    : "hover:bg-muted/50"
                }`}
              >
                <Checkbox
                  checked={selected.has(repo.url)}
                  onCheckedChange={() => handleToggleSelect(repo.url)}
                  disabled={repo.alreadyExists}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <a
                      href={repo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-primary hover:underline"
                    >
                      {repo.fullName}
                    </a>
                    {repo.language && (
                      <Badge variant="outline">{repo.language}</Badge>
                    )}
                    {repo.alreadyExists && (
                      <Badge variant="secondary">{t.alreadyExists}</Badge>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
                    {repo.description}
                  </p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                    <span>⭐ {repo.stars.toLocaleString()}</span>
                    <span>🍴 {repo.forks.toLocaleString()}</span>
                    <span>{new Date(repo.updatedAt).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            {t.cancel}
          </Button>
          <Button
            onClick={handleImport}
            disabled={isImporting || selected.size === 0 || !categoryId}
          >
            {isImporting ? t.loading : `${t.importSelected} (${selected.size})`}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
