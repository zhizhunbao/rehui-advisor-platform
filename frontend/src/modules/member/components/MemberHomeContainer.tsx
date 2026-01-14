// Member 首页容器组件
import type { Language, TopicCategory, Topic } from "@/common/types";
import { advisorLocales } from "@/common/i18n";
import { getIcon } from "@/common/helper";
import MemberTopicCard from "./MemberTopicCard";
import MemberChatInput from "./MemberChatInput";

interface MemberHomeContainerProps {
  lang: Language;
  categories: TopicCategory[];
  isLoading: boolean;
  error: string | null;
  handleTopicClick: (topic: Topic) => void;
  handleQuickSearch: (query: string) => void;
}

export function MemberHomeContainer({
  lang,
  categories,
  isLoading,
  error,
  handleTopicClick,
  handleQuickSearch,
}: MemberHomeContainerProps) {
  const t = advisorLocales[lang];

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
            onSend={handleQuickSearch}
            isLoading={false}
            lang={lang}
          />
        </div>

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
                      onClick={handleTopicClick}
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
