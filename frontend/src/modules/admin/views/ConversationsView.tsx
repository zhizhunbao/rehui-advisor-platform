// Admin 会话管理页面
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

export default function ConversationsView() {
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
    handleReset,
  } = useConversations();

  return (
    <AdminViewContainer>
      <AdminViewTitle />
      <AdminConversationFilter
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
      >
        <AdminConversationTable
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
        />
      </AdminViewContent>
      <AdminConversationDetailDialog
        conversation={selectedConversation}
        open={showDetail}
        onOpenChange={setShowDetail}
      />
    </AdminViewContainer>
  );
}
