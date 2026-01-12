import type { Language } from "../types";
import { memberLocales } from "../locales";

interface FooterProps {
  lang: Language;
}

const Footer: React.FC<FooterProps> = ({ lang }) => {
  const t = memberLocales[lang];
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

export default Footer;
