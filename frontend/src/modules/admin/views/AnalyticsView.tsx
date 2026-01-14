// Admin 数据分析页面
import { useAnalytics } from "../hooks/useAnalytics";
import { AdminAnalyticsHeader } from "../components/AdminAnalyticsHeader";
import { AdminAnalyticsStats } from "../components/AdminAnalyticsStats";
import { AdminAnalyticsCharts } from "../components/AdminAnalyticsCharts";
import {
  AdminViewContainer,
  AdminViewContent,
} from "../components/AdminViewLayout";

export default function AnalyticsView() {
  const { summary, isLoading } = useAnalytics();

  return (
    <AdminViewContainer>
      <AdminAnalyticsHeader />
      <AdminViewContent isLoading={isLoading} isEmpty={false}>
        <AdminAnalyticsStats summary={summary} />
        <AdminAnalyticsCharts summary={summary} />
      </AdminViewContent>
    </AdminViewContainer>
  );
}
