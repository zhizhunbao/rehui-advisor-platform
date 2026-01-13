// Member 消息气泡组件 - Props: message, lang, onSuggestionClick, onRegenerate
import { useState, useMemo } from "react";
import type {
  Message,
  Language,
  ChartData,
  GroundingSource,
} from "@/common/types";
import { advisorLocales } from "@/common/i18n";
import {
  Copy,
  Check,
  ExternalLink,
  CheckCircle2,
  UserSearch,
  ThumbsUp,
  ThumbsDown,
  Share,
  RotateCw,
  MoreHorizontal,
} from "lucide-react";
import MemberDataVisualizer from "./MemberDataVisualizer";

interface MemberMessageBubbleProps {
  message: Message;
  lang: Language;
  onSuggestionClick?: (question: string) => void;
  onRegenerate?: () => void;
}

const parseMessageContent = (content: string) => {
  let chartData: ChartData | null = null;
  const suggestedQuestions: string[] = [];
  const options: string[] = [];
  let currentStep = "";

  const stepMatch = content.match(/\[STEP:\s*(\d+\/\d+)\]/);
  if (stepMatch) currentStep = stepMatch[1];

  const chartMatch = content.match(/\[CHART_DATA:\s*(\{.*?\})\]/);
  if (chartMatch) {
    try {
      chartData = JSON.parse(chartMatch[1]);
    } catch {
      /* ignore */
    }
  }

  const suggestMatches = Array.from(
    content.matchAll(/\[SUGGEST:\s*"(.*?)"\]/g)
  );
  suggestMatches.forEach((m) => suggestedQuestions.push(m[1]));

  const optionMatches = Array.from(content.matchAll(/\[OPTION:\s*"(.*?)"\]/g));
  optionMatches.forEach((m) => options.push(m[1]));

  const cleanContent = content
    .replace(/\[STEP:\s*\d+\/\d+\]/g, "")
    .replace(/\[CHART_DATA:\s*\{.*?\}\]/g, "")
    .replace(/\[SUGGEST:\s*".*?"\]/g, "")
    .replace(/\[OPTION:\s*".*?"\]/g, "")
    .trim();

  return { cleanContent, chartData, suggestedQuestions, options, currentStep };
};

const formatMarkdown = (content: string, lang: Language) => {
  if (!content) return "";
  let html = content;

  const isZh = lang === "zh";
  const insightHeader = isZh ? "STAGE 3: 核心洞察" : "STAGE 3: CORE INSIGHT";
  const reportHeader = isZh ? "深度调研报告" : "RESEARCH SYNTHESIS";

  html = html.replace(
    /⚡️ \[(核心洞察|Core Insight)\]/g,
    `<div class="text-[10px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-[0.2em] mb-4">${insightHeader}</div>`
  );
  html = html.replace(
    /💡 \[(深度报告|Depth Report)\]/g,
    `<div class="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-4 mt-10">${reportHeader}</div>`
  );
  html = html.replace(
    /(现在开始为您抓取|正在为您执行调研|Starting to crawl|I am now retrieving|Connecting to real-time)/g,
    '<span class="text-emerald-600 dark:text-emerald-400 font-bold">$1</span>'
  );
  html = html.replace(
    /\*\*(.*?)\*\*/g,
    '<strong class="font-bold text-slate-900 dark:text-white">$1</strong>'
  );
  html = html.replace(
    /^### (.*$)/gm,
    '<h3 class="text-xl font-extrabold mt-10 mb-4 text-slate-900 dark:text-white tracking-tight">$1</h3>'
  );
  html = html.replace(
    /^\s*[-*+]\s+(.*)$/gm,
    '<li class="ml-4 list-disc my-3 pl-2 text-slate-700 dark:text-slate-300">$1</li>'
  );

  return html
    .split("\n\n")
    .map((p) => {
      if (p.trim().startsWith("<")) return p;
      return `<p class="mb-4 leading-[1.7] text-slate-700 dark:text-slate-200">${p.replace(
        /\n/g,
        "<br/>"
      )}</p>`;
    })
    .join("");
};

export default function MemberMessageBubble({
  message,
  lang,
  onSuggestionClick,
  onRegenerate,
}: MemberMessageBubbleProps) {
  const isAssistant = message.role === "assistant";
  const [copied, setCopied] = useState(false);
  const t = advisorLocales[lang];

  const { cleanContent, chartData, suggestedQuestions, options, currentStep } =
    useMemo(() => parseMessageContent(message.content), [message.content]);
  const formattedContent = useMemo(
    () => formatMarkdown(cleanContent, lang),
    [cleanContent, lang]
  );

  if (message.metadata?.hidden) return null;

  return (
    <div className="w-full flex justify-center py-4 animate-in">
      <div
        className={`w-full max-w-3xl px-4 flex gap-4 ${
          !isAssistant ? "flex-row-reverse" : "flex-row"
        }`}
      >
        {isAssistant && (
          <div className="shrink-0 pt-1 hidden sm:block">
            <div className="w-8 h-8 rounded-lg bg-slate-900 dark:bg-white/10 flex items-center justify-center border border-slate-200 dark:border-white/5 shadow-sm">
              <UserSearch className="w-4 h-4 text-white dark:text-slate-200" />
            </div>
          </div>
        )}

        <div
          className={`flex-1 min-w-0 ${
            !isAssistant ? "flex flex-col items-end" : ""
          }`}
        >
          {isAssistant && currentStep && !message.isStreaming && (
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-blue-600/10 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">
                {t.stepLabel} {currentStep}
              </div>
            </div>
          )}

          <div
            className={`text-[15px] max-w-full ${
              !isAssistant
                ? "bg-[#3c3c3c] dark:bg-[#2f2f2f] rounded-[1.2rem] px-5 py-3 text-white shadow-sm inline-block"
                : "w-full text-slate-800 dark:text-slate-200"
            }`}
          >
            <div dangerouslySetInnerHTML={{ __html: formattedContent }} />

            {isAssistant && options.length > 0 && !message.isStreaming && (
              <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-2">
                {options.map((opt, i) => (
                  <button
                    key={i}
                    onClick={() => onSuggestionClick?.(opt)}
                    className="flex items-center justify-between text-left px-4 py-3 rounded-xl bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-200 hover:border-blue-500 transition-all active:scale-[0.98]"
                  >
                    <span className="font-semibold text-[13px]">{opt}</span>
                    <CheckCircle2 className="w-4 h-4 text-slate-200 dark:text-white/10" />
                  </button>
                ))}
              </div>
            )}

            {isAssistant && chartData && chartData.values?.length > 0 && (
              <MemberDataVisualizer data={chartData} lang={lang} />
            )}
            {isAssistant && message.isStreaming && (
              <span className="inline-block w-1 h-5 ml-1 bg-blue-500/40 rounded-full animate-pulse align-middle" />
            )}
          </div>

          {isAssistant && !message.isStreaming && (
            <div className="mt-4 flex flex-col gap-4">
              {(suggestedQuestions.length > 0 ||
                (message.sources && message.sources.length > 0)) && (
                <div className="space-y-4 border-l-2 border-slate-100 dark:border-white/5 pl-4 py-1">
                  {suggestedQuestions.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {suggestedQuestions.map((q, i) => (
                        <button
                          key={i}
                          onClick={() => onSuggestionClick?.(q)}
                          className="text-[12px] px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-white/5 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-white/10 transition-colors font-medium"
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  )}
                  {message.sources && message.sources.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {message.sources.map((s: GroundingSource, i: number) => (
                        <a
                          key={i}
                          href={s.uri}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-1.5 text-[11px] text-blue-500 hover:underline"
                        >
                          <ExternalLink className="w-3 h-3" />
                          <span className="truncate max-w-[150px]">
                            {s.title}
                          </span>
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              )}

              <div className="flex items-center gap-1 text-slate-400">
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(cleanContent);
                    setCopied(true);
                    setTimeout(() => setCopied(false), 2000);
                  }}
                  className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
                >
                  {copied ? (
                    <Check className="w-4 h-4 text-emerald-500" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </button>
                <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors">
                  <ThumbsUp className="w-4 h-4" />
                </button>
                <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors">
                  <ThumbsDown className="w-4 h-4" />
                </button>
                <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors">
                  <Share className="w-4 h-4" />
                </button>
                <button
                  onClick={onRegenerate}
                  className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
                >
                  <RotateCw className="w-4 h-4" />
                </button>
                <button className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
