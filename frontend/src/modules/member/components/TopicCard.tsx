import type { Topic } from "../types";
import { getIcon } from "../utils/icons";

interface TopicCardProps {
  topic: Topic;
  onClick: (topic: Topic) => void;
}

const TopicCard: React.FC<TopicCardProps> = ({ topic, onClick }) => {
  return (
    <div
      onClick={() => onClick(topic)}
      className="group relative bg-white dark:bg-[#2f2f2f]/40 backdrop-blur-sm border border-slate-200 dark:border-white/5 rounded-2xl p-5 cursor-pointer hover:border-blue-500/50 dark:hover:border-blue-400/50 hover:shadow-xl hover:shadow-blue-500/10 transition-all duration-500 transform hover:-translate-y-1.5 active:scale-95 shadow-sm overflow-hidden"
    >
      <div
        className={`absolute -right-4 -top-4 w-20 h-20 blur-3xl opacity-0 group-hover:opacity-20 transition-opacity duration-700 ${topic.color}`}
      />

      <div
        className={`w-11 h-11 ${topic.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-500 shadow-lg shadow-black/10`}
      >
        {getIcon(topic.icon, "text-white w-5 h-5")}
      </div>

      <h3 className="text-[16px] font-bold text-slate-900 dark:text-white mb-1.5 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors tracking-tight">
        {topic.title}
      </h3>
      <p className="text-[13px] text-slate-500 dark:text-slate-400 leading-tight line-clamp-2 font-medium">
        {topic.description}
      </p>

      <div className="mt-4 flex items-center gap-1 text-[10px] font-extrabold text-blue-600 dark:text-blue-500 opacity-0 group-hover:opacity-100 transition-all transform translate-y-2 group-hover:translate-y-0 uppercase tracking-widest">
        <span>Get Advice</span>
        <svg
          className="w-3 h-3"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={3}
            d="M14 5l7 7m0 0l-7 7m7-7H3"
          />
        </svg>
      </div>
    </div>
  );
};

export default TopicCard;
