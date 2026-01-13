import { useState, useEffect } from "react";
import type { Topic, Language } from "@/common/types";
import MemberTopicCard from "@/modules/member/components/MemberTopicCard";
import MemberChatInput from "@/modules/member/components/MemberChatInput";
import { advisorLocales } from "@/common/i18n";
import {
  domainService,
  type TopicCategory,
  type ProductLine,
} from "@/modules/member/services/domain.service";
import { getIcon } from "@/common/helper";

interface HomeViewProps {
  lang: Language;
  onTopicClick: (topic: Topic) => void;
  onQuickSearch: (query: string) => void;
}

export default function HomeView({
  lang,
  onTopicClick,
  onQuickSearch,
}: HomeViewProps) {
  const t = advisorLocales[lang];
  const [productLines, setProductLines] = useState<ProductLine[]>([]);
  const [activeLineId, setActiveLineId] = useState<string | null>(null);
  const [categories, setCategories] = useState<TopicCategory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProductLines = async () => {
      try {
        const lines = await domainService.getProductLines();
        setProductLines(lines);
        if (lines.length > 0) {
          setActiveLineId(lines[0].id);
        }
      } catch {
        setError(lang === "zh" ? "加载失败" : "Failed to load");
      }
    };
    fetchProductLines();
  }, [lang]);

  useEffect(() => {
    if (!activeLineId) return;
    const fetchCategories = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await domainService.getGroupedTopics(lang, activeLineId);
        setCategories(data);
      } catch {
        setError(lang === "zh" ? "加载失败" : "Failed to load");
      } finally {
        setIsLoading(false);
      }
    };
    fetchCategories();
  }, [lang, activeLineId]);

  const activeLine = productLines.find((p) => p.id === activeLineId);

  return (
    <div className="w-full min-h-full flex flex-col items-center bg-white dark:bg-admin-bg-dark px-6 py-12 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-40 dark:opacity-20">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-400/10 blur-[120px] rounded-full" />
        <div className="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-indigo-400/10 blur-[120px] rounded-full" />
      </div>

      <div className="w-full max-w-5xl flex flex-col items-center relative z-10">
        <div className="text-center mb-8 max-w-3xl">
          <h1 className="text-3xl md:text-5xl font-black text-slate-900 dark:text-white mb-4 tracking-tighter leading-[1.1]">
            {t.subtitle}{" "}
            <span className="bg-clip-text text-transparent bg-linear-to-r from-blue-600 to-indigo-500">
              {t.subtitleSuffix}
            </span>
          </h1>
        </div>

        <div className="w-full max-w-2xl mb-10">
          <MemberChatInput
            onSend={onQuickSearch}
            isLoading={false}
            placeholder={t.placeholder}
          />
        </div>

        {productLines.length > 1 && (
          <div className="flex gap-3 mb-8">
            {productLines.map((line) => {
              const isActive = line.id === activeLineId;
              return (
                <button
                  key={line.id}
                  onClick={() => setActiveLineId(line.id)}
                  className={`flex items-center gap-2 px-5 py-2.5 rounded-full font-medium transition-all ${
                    isActive
                      ? "bg-blue-600 text-white shadow-lg"
                      : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"
                  }`}
                >
                  {getIcon(line.icon, "w-4 h-4")}
                  <span>{lang === "zh" ? line.name : line.nameEn}</span>
                </button>
              );
            })}
          </div>
        )}

        {activeLine && (
          <p className="text-slate-500 dark:text-slate-400 mb-8 text-center">
            {lang === "zh" ? activeLine.description : activeLine.descriptionEn}
          </p>
        )}

        {isLoading ? (
          <div className="text-slate-500">{t.loading}</div>
        ) : error ? (
          <div className="text-red-500">{error}</div>
        ) : (
          <div className="w-full space-y-8">
            {categories.map((category) => (
              <div key={category.id}>
                <h2 className="text-lg font-semibold text-slate-700 dark:text-slate-300 mb-4 flex items-center gap-2">
                  {getIcon(category.icon, "w-5 h-5")}
                  {category.name}
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  {category.topics.map((topic) => (
                    <MemberTopicCard
                      key={topic.id}
                      topic={topic}
                      onClick={onTopicClick}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
