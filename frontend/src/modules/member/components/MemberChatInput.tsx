// Member 聊天输入组件 - Props: onSend, isLoading, prompts, promptCategories, onSearchPrompts
import { useState, useRef, useEffect } from "react";
import { ArrowUp, Sparkles } from "lucide-react";
import MemberPromptSelector, {
  type Prompt,
  type PromptCategory,
} from "./MemberPromptSelector";
import type { Language } from "@/common/types";
import { advisorLocales } from "@/common/i18n";

interface MemberChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  placeholder?: string;
  disabled?: boolean;
  disabledPlaceholder?: string;
  lang?: Language;
  prompts?: Prompt[];
  promptCategories?: PromptCategory[];
  isLoadingPrompts?: boolean;
  onSearchPrompts?: (search: string, category: string) => void;
}

const MemberChatInput: React.FC<MemberChatInputProps> = ({
  onSend,
  isLoading,
  placeholder,
  disabled,
  disabledPlaceholder,
  lang = "zh",
  prompts = [],
  promptCategories = [],
  isLoadingPrompts = false,
  onSearchPrompts,
}) => {
  const t = advisorLocales[lang];
  const [text, setText] = useState("");
  const [showPromptSelector, setShowPromptSelector] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (text.trim() && !isLoading && !disabled) {
      onSend(text.trim());
      setText("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handlePromptSelect = (prompt: Prompt) => {
    if (prompt.template) {
      setText(prompt.template);
      textareaRef.current?.focus();
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  }, [text]);

  const displayPlaceholder =
    disabled && disabledPlaceholder ? disabledPlaceholder : placeholder;

  return (
    <div className="relative w-full">
      <div
        className={`
        flex items-end gap-3 bg-white dark:bg-[#2f2f2f] 
        rounded-[32px] p-2 pr-2.5 pl-4 transition-all duration-500
        border border-slate-200/60 dark:border-white/5
        shadow-[0_10px_40px_-10px_rgba(0,0,0,0.05)] dark:shadow-[0_20px_50px_-12px_rgba(0,0,0,0.3)]
        ${disabled ? "opacity-50 cursor-not-allowed" : ""}
      `}
      >
        <button
          onClick={() => setShowPromptSelector(true)}
          disabled={disabled || isLoading}
          className="mb-1.5 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 bg-linear-to-r from-purple-500 to-blue-500 text-white hover:scale-105 hover:shadow-lg disabled:opacity-50"
          title={t.selectPrompt}
        >
          <Sparkles className="w-5 h-5" />
        </button>

        <textarea
          ref={textareaRef}
          rows={1}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={displayPlaceholder}
          className="flex-1 bg-transparent border-none focus:ring-0 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 resize-none py-3.5 text-[15px] leading-relaxed max-h-[200px] scrollbar-hide outline-none"
          disabled={disabled || isLoading}
        />

        <button
          onClick={handleSend}
          disabled={!text.trim() || isLoading || disabled}
          className={`
            mb-1.5 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300
            ${
              text.trim() && !isLoading
                ? "bg-slate-900 dark:bg-white text-white dark:text-black hover:scale-105 shadow-lg"
                : "bg-slate-100 dark:bg-slate-800 text-slate-300 dark:text-slate-600"
            }
          `}
        >
          {isLoading ? (
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
          ) : (
            <ArrowUp className="w-5 h-5" strokeWidth={3} />
          )}
        </button>
      </div>

      {showPromptSelector && onSearchPrompts && (
        <MemberPromptSelector
          lang={lang}
          prompts={prompts}
          categories={promptCategories}
          isLoading={isLoadingPrompts}
          onSelect={handlePromptSelect}
          onClose={() => setShowPromptSelector(false)}
          onSearch={onSearchPrompts}
        />
      )}
    </div>
  );
};

export default MemberChatInput;
