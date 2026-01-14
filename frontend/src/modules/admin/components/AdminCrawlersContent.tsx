// Admin 爬虫内容区域
import type { CrawlSource, CrawlTask } from "@/common/types";
import { AdminCrawlerSourceList } from "./AdminCrawlerSourceList";
import { AdminCrawlerTaskList } from "./AdminCrawlerTaskList";

interface Props {
  sources: CrawlSource[];
  tasks: CrawlTask[];
  selectedSourceId: string | null;
  onSelect: (id: string) => void;
  onRun: (id: string) => void;
  onDelete: (id: string) => void;
}

export function AdminCrawlersContent({
  sources,
  tasks,
  selectedSourceId,
  onSelect,
  onRun,
  onDelete,
}: Props) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <AdminCrawlerSourceList
        sources={sources}
        selectedSourceId={selectedSourceId}
        onSelect={onSelect}
        onRun={onRun}
        onDelete={onDelete}
      />
      <AdminCrawlerTaskList tasks={tasks} />
    </div>
  );
}
