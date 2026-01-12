import type { ChartData, Language } from "../types";

interface DataVisualizerProps {
  data: ChartData;
  lang: Language;
}

const DataVisualizer: React.FC<DataVisualizerProps> = ({ data, lang }) => {
  if (!data || !data.values || data.values.length === 0) return null;

  const maxValue = Math.max(...data.values, 1);
  const isZh = lang === "zh";

  return (
    <div className="my-10 p-8 bg-slate-50/30 dark:bg-white/[0.02] border border-slate-200/50 dark:border-white/5 rounded-[2rem] animate-in">
      <div className="flex items-center justify-between mb-10">
        <div className="space-y-1">
          <h4 className="text-[13px] font-black uppercase tracking-widest text-slate-900 dark:text-white">
            {data.title || (isZh ? "数据对比报告" : "Comparison Report")}
          </h4>
          <p className="text-[10px] text-slate-400 font-bold uppercase tracking-[0.2em]">
            {isZh ? "实时情报量化分析" : "Live Intelligence Analysis"}
          </p>
        </div>
        <div className="text-[11px] font-black text-blue-600 bg-blue-50 dark:bg-blue-500/10 px-3 py-1 rounded-full uppercase tracking-tighter">
          {data.unit || (isZh ? "数值" : "Value")}
        </div>
      </div>

      <div className="space-y-8">
        {data.labels.map((label, i) => {
          const val = data.values[i] ?? 0;
          const percentage = (val / maxValue) * 100;
          return (
            <div key={i} className="space-y-2.5">
              <div className="flex justify-between text-[13px] font-bold">
                <span className="text-slate-500 dark:text-slate-400">
                  {label}
                </span>
                <span className="text-slate-900 dark:text-white tabular-nums">
                  {val.toLocaleString()}
                </span>
              </div>
              <div className="h-1 bg-slate-200 dark:bg-white/5 rounded-full overflow-hidden">
                <div
                  className="h-full bg-slate-900 dark:bg-blue-500 rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DataVisualizer;
