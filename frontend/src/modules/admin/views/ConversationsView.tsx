// Admin 会话管理页面 - 组合组件，无 className 和直接 API 调用
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { useConversations } from "../hooks/useConversations";
import { AdminConversationFilter } from "../components/AdminConversationFilter";
import { AdminConversationTable } from "../components/AdminConversationTable";
import { AdminConversationDetailDialog } from "../components/AdminConversationDetailDialog";
import { AdminLoadMoreIndicator } from "../components/AdminLoadMoreIndicator";
import {
  AdminViewContainer,
  AdminViewTitle,
  AdminViewContent,
} from "../components/AdminViewLayout";

interface ConversationsViewProps {
  lang: Language;
}

export default function ConversationsView({ lang }: ConversationsViewProps) {
  const t = adminLocales[lang];
  const {
    conversations,
    selectedConversation,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    showDetail,
    setShowDetail,
    userId,
    setUserId,
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    refresh,
    fetchConversationDetail,
    deleteConversation,
    resetFilters,
  } = useConversations();

  const handleReset = () => {
    resetFilters();
    refresh();
  };

  return (
    <AdminViewContainer>
      <AdminViewTitle title={t.conversations} />
      <AdminConversationFilter
        lang={lang}
        userId={userId}
        startDate={startDate}
        endDate={endDate}
        onUserIdChange={setUserId}
        onStartDateChange={setStartDate}
        onEndDateChange={setEndDate}
        onFilter={refresh}
        onReset={handleReset}
      />
      <AdminViewContent
        isLoading={isLoading}
        isEmpty={conversations.length === 0}
        loadingText={t.loading}
        emptyText={t.noData}
      >
        <AdminConversationTable
          lang={lang}
          conversations={conversations}
          onViewDetail={fetchConversationDetail}
          onDelete={deleteConversation}
        />
        <AdminLoadMoreIndicator
          loadMoreRef={loadMoreRef}
          hasMore={hasMore}
          isLoading={isLoading}
          total={total}
          count={conversations.length}
          lang={lang}
        />
      </AdminViewContent>
      <AdminConversationDetailDialog
        lang={lang}
        conversation={selectedConversation}
        open={showDetail}
        onOpenChange={setShowDetail}
      />
    </AdminViewContainer>
  );
}
