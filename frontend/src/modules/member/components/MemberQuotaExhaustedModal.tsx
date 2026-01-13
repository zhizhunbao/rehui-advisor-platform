// Member 配额耗尽弹窗组件 - Props: lang, quotaStatus, onClose, onNavigate
import type { Language, AppView, QuotaStatus } from "@/common/types";
import { advisorLocales } from "@/common/i18n";
import { AlertCircle, X, UserPlus, Sparkles } from "lucide-react";

interface MemberQuotaExhaustedModalProps {
  lang: Language;
  quotaStatus: QuotaStatus | null;
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (view: AppView) => void;
}

const MemberQuotaExhaustedModal: React.FC<MemberQuotaExhaustedModalProps> = ({
  lang,
  quotaStatus,
  isOpen,
  onClose,
  onNavigate,
}) => {
  const t = advisorLocales[lang];
  const isAnonymous = quotaStatus?.userType === "ANONYMOUS";

  if (!isOpen) return null;

  const handleAction = () => {
    if (isAnonymous) {
      onNavigate("register");
    } else {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      <div className="relative bg-white dark:bg-slate-900 rounded-2xl shadow-2xl max-w-md w-full mx-4 overflow-hidden">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="p-8 text-center">
          <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
            <AlertCircle className="w-8 h-8 text-amber-500" />
          </div>

          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
            {isAnonymous ? t.quotaExhaustedAnonymous : t.quotaExhausted}
          </h3>

          <p className="text-slate-500 dark:text-slate-400 mb-6">
            {isAnonymous ? t.quotaExhaustedAnonymousDesc : t.quotaExhaustedDesc}
          </p>

          <button
            onClick={handleAction}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors"
          >
            {isAnonymous ? (
              <>
                <UserPlus className="w-5 h-5" />
                {t.registerForMore}
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                {t.upgradeNow}
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default MemberQuotaExhaustedModal;
