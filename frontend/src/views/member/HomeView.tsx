import { useState, useEffect } from "react";
import type { Topic, Language } from "@/modules/member/types";
import { TopicCard, ChatInput } from "@/modules/member/components";
import { memberLocales } from "@/modules/member/locales";

interface HomeViewProps {
  lang: Language;
  onTopicClick: (topic: Topic) => void;
  onQuickSearch: (query: string) => void;
}

const API_BASE = import.meta.env.VITE_API_URL || "/api";

// Icon 映射
const ICON_MAP: Record<string, string> = {
  plane: "Plane",
  building: "Hotel",
  briefcase: "Briefcase",
  car: "Car",
  home: "Home",
  shield: "ShieldCheck",
  "graduation-cap": "GraduationCap",
  "trending-up": "TrendingUp",
};

// Color 映射
const COLOR_MAP: Record<string, string> = {
  "#3B82F6": "bg-blue-500",
  "#10B981": "bg-emerald-500",
  "#6366F1": "bg-indigo-500",
  "#F97316": "bg-orange-500",
  "#EF4444": "bg-rose-500",
  "#06B6D4": "bg-cyan-500",
  "#8B5CF6": "bg-purple-500",
  "#F59E0B": "bg-amber-500",
};

export default function HomeView({
  lang,
  onTopicClick,
  onQuickSearch,
}: HomeViewProps) {
  const t = memberLocales[lang];
  const [topics, setTopics] = useState<Topic[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDomains = async () => {
      try {
        const res = await fetch(`${API_BASE}/domains/active`);
        const json = await res.json();
        if (json.success && json.data) {
          const mapped: Topic[] = json.data.map(
            (d: Record<string, string>) => ({
              id: d.code || d.id,
              title: lang === "zh" ? d.name : d.nameEn,
              description: lang === "zh" ? d.description : d.descriptionEn,
              icon: ICON_MAP[d.icon] || "Circle",
              color: COLOR_MAP[d.color] || "bg-slate-500",
              prompt: lang === "zh" ? d.prompt : d.promptEn,
            })
          );
          setTopics(mapped);
        }
      } catch (err) {
        console.error("Failed to fetch domains:", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDomains();
  }, [lang]);

  return (
    <div className="w-full min-h-full flex flex-col items-center justify-center bg-white dark:bg-[#212121] px-6 py-12 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-40 dark:opacity-20">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-400/10 blur-[120px] rounded-full" />
        <div className="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-indigo-400/10 blur-[120px] rounded-full" />
      </div>

      <div className="w-full max-w-4xl flex flex-col items-center relative z-10 animate-in">
        <div className="text-center mb-10 max-w-3xl">
          <h1 className="text-4xl md:text-6xl font-black text-slate-900 dark:text-white mb-6 tracking-tighter leading-[1.1]">
            {t.subtitle}{" "}
            <span className="bg-clip-text text-transparent bg-linear-to-r from-blue-600 to-indigo-500">
              {t.subtitleSuffix}
            </span>
          </h1>
        </div>

        <div className="w-full max-w-2xl mb-16">
          <ChatInput
            onSend={onQuickSearch}
            isLoading={false}
            placeholder={t.placeholder}
          />
        </div>

        {isLoading ? (
          <div className="text-slate-500">{t.loading}</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full">
            {topics.map((topic) => (
              <TopicCard key={topic.id} topic={topic} onClick={onTopicClick} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
