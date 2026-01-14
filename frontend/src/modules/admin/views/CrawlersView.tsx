// Admin 爬虫管理页面
import { useCrawlers } from "../hooks/useCrawlers";
import { AdminCrawlersHeader } from "../components/AdminCrawlersHeader";
import { AdminCrawlersContent } from "../components/AdminCrawlersContent";
import {
  AdminViewContainer,
  AdminViewContent,
} from "../components/AdminViewLayout";

export default function CrawlersView() {
  const {
    sources,
    filteredTasks,
    isLoading,
    selectedSourceId,
    setSelectedSourceId,
    handleRunTask,
    handleDeleteSource,
  } = useCrawlers();

  return (
    <AdminViewContainer>
      <AdminCrawlersHeader onCreate={() => {}} />
      <AdminViewContent isLoading={isLoading} isEmpty={false}>
        <AdminCrawlersContent
          sources={sources}
          tasks={filteredTasks}
          selectedSourceId={selectedSourceId}
          onSelect={setSelectedSourceId}
          onRun={handleRunTask}
          onDelete={handleDeleteSource}
        />
      </AdminViewContent>
    </AdminViewContainer>
  );
}
