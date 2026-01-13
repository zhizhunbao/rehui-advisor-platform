// Member 底部组件 - Props: lang
import type { Language } from "@/common/types";
import { advisorLocales } from "@/common/i18n";

interface MemberFooterProps {
  lang: Language;
}

const MemberFooter: React.FC<MemberFooterProps> = ({ lang }) => {
  const t = advisorLocales[lang];
  return (
    <footer className="w-full py-4 px-6 mt-auto">
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-slate-400 dark:text-slate-500">
        <div className="text-[11px] font-bold uppercase tracking-widest">
          {t.copyright}
        </div>
        <div className="flex gap-6">
          <a
            href="#"
            className="text-[12px] font-medium hover:text-slate-900 dark:hover:text-white transition-colors"
          >
            {t.about}
          </a>
          <a
            href="#"
            className="text-[12px] font-medium hover:text-slate-900 dark:hover:text-white transition-colors"
          >
            {t.terms}
          </a>
          <a
            href="#"
            className="text-[12px] font-medium hover:text-slate-900 dark:hover:text-white transition-colors"
          >
            {t.privacy}
          </a>
        </div>
      </div>
    </footer>
  );
};

export default MemberFooter;
