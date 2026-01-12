import { useState, useCallback, useEffect } from "react";
import { adminLocales, type Language } from "@/locales";
import { getApiBase, getAuthHeaders } from "@/modules/admin/utils/api";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Checkbox } from "@/libs/shadcn/ui/checkbox";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/libs/shadcn/ui/tabs";
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

interface GitHubRepo {
  url: string;
  name: string;
  full_name: string;
  description: string;
  stars: number;
  forks: number;
  language: string;
  topics: string[];
  updated_at: string;
  owner: string;
  repo: string;
  already_exists: boolean;
}

interface DomainKeywords {
  domain: string;
  name_zh: string;
  name_en: string;
  keywords: string[];
}

interface Category {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

interface GitHubDiscoverModalProps {
  lang: Language;
  categories: Category[];
  onClose: () => void;
  onSuccess: () => void;
}

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export function GitHubDiscoverModal({
  lang,
  categories,
  onClose,
  onSuccess,
}: GitHubDiscoverModalProps) {
  const t = adminLocales[lang];

  const [activeTab, setActiveTab] = useState("manual");
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("stars");
  const [perPage, setPerPage] = useState("30");
  const [categoryId, setCategoryId] = useState("");
  const [domainId, setDomainId] = useState("");
  const [domains, setDomains] = useState<
    { id: string; code: string; name: string; nameEn: string }[]
  >([]);

  const [isSearching, setIsSearching] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [results, setResults] = useState<GitHubRepo[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [error, setError] = useState("");

  const [domainKeywords, setDomainKeywords] = useState<DomainKeywords[]>([]);
  const [selectedDomain, setSelectedDomain] = useState("");
  const [isAutoDiscovering, setIsAutoDiscovering] = useState(false);

  useEffect(() => {
    const fetchDomainKeywords = async () => {
      try {
        const res = await fetch(`${API_BASE}/data-sources/discover/domains`, {
          headers: getHeaders(),
        });
        const json = await res.json();
        if (json.success) {
          setDomainKeywords(json.data);
        }
      } catch {
        // ignore
      }
    };
    fetchDomainKeywords();
  }, []);

  // 当 categoryId 变化时，获取对应的领域列表
  useEffect(() => {
    const fetchDomains = async () => {
      if (!categoryId) {
        setDomains([]);
        setDomainId("");
        return;
      }
      try {
        const res = await fetch(
          `${API_BASE}/data-sources/categories/${categoryId}/domains`,
          { headers: getHeaders() }
        );
        const json = await res.json();
        if (json.success) {
          setDomains(json.data);
        }
      } catch {
        setDomains([]);
      }
    };
    fetchDomains();
    setDomainId("");
  }, [categoryId]);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;
    setIsSearching(true);
    setError("");
    setResults([]);
    setSelected(new Set());
    try {
      const res = await fetch(`${API_BASE}/data-sources/discover/github`, {
        method: "POST",
        headers: { ...getHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify({
          query: query.trim(),
          sort,
          order: "desc",
          per_page: parseInt(perPage),
        }),
      });
      const json = await res.json();
      if (json.success) {
        setResults(json.data);
      } else {
        setError(json.error?.message || "Search failed");
      }
    } catch {
      setError("Network error");
    } finally {
      setIsSearching(false);
    }
  }, [query, sort, perPage]);

  const handleAutoDiscover = useCallback(async () => {
    if (!selectedDomain) return;
    setIsAutoDiscovering(true);
    setError("");
    setResults([]);
    setSelected(new Set());
    try {
      const res = await fetch(
        `${API_BASE}/data-sources/discover/auto/${selectedDomain}?limit_per_keyword=15`,
        { method: "POST", headers: getHeaders() }
      );
      const json = await res.json();
      if (json.success) {
        setResults(json.data.results);
        if (!categoryId) setCategoryId(selectedDomain);
      } else {
        setError(json.error?.message || "Auto discover failed");
      }
    } catch {
      setError("Network error");
    } finally {
      setIsAutoDiscovering(false);
    }
  }, [selectedDomain, categoryId]);

  const handleToggleSelect = (url: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(url)) next.delete(url);
      else next.add(url);
      return next;
    });
  };

  const selectableCount = results.filter((r) => !r.already_exists).length;

  const handleSelectAll = () => {
    const selectable = results.filter((r) => !r.already_exists);
    if (selected.size === selectable.length) setSelected(new Set());
    else setSelected(new Set(selectable.map((r) => r.url)));
  };

  const handleImport = async () => {
    if (selected.size === 0 || !categoryId) return;
    setIsImporting(true);
    try {
      const items = results.filter((r) => selected.has(r.url));
      const res = await fetch(`${API_BASE}/data-sources/discover/import`, {
        method: "POST",
        headers: { ...getHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify({
          items,
          category_id: categoryId,
          domain_id: domainId || null,
        }),
      });
      const json = await res.json();
      if (json.success) {
        alert(
          t.importedCount
            .replace("{added}", json.data.added)
            .replace("{skipped}", json.data.skipped)
        );
        onSuccess();
        onClose();
      }
    } catch {
      setError("Import failed");
    } finally {
      setIsImporting(false);
    }
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
                        {lang === "zh" ? d.name_zh : d.name_en} (
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

        {/* Category & Results */}
        <div className="space-y-4 flex-1 overflow-hidden flex flex-col">
          <div className="flex gap-4">
            <div className="w-48">
              <label className="text-sm text-muted-foreground mb-1 block">
                {t.category} *
              </label>
              <Select value={categoryId} onValueChange={setCategoryId}>
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
                  repo.already_exists
                    ? "opacity-50 bg-muted"
                    : "hover:bg-muted/50"
                }`}
              >
                <Checkbox
                  checked={selected.has(repo.url)}
                  onCheckedChange={() => handleToggleSelect(repo.url)}
                  disabled={repo.already_exists}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <a
                      href={repo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-primary hover:underline"
                    >
                      {repo.full_name}
                    </a>
                    {repo.language && (
                      <Badge variant="outline">{repo.language}</Badge>
                    )}
                    {repo.already_exists && (
                      <Badge variant="secondary">{t.alreadyExists}</Badge>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
                    {repo.description}
                  </p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                    <span>⭐ {repo.stars.toLocaleString()}</span>
                    <span>🍴 {repo.forks.toLocaleString()}</span>
                    <span>
                      {new Date(repo.updated_at).toLocaleDateString()}
                    </span>
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
