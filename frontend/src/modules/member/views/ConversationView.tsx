// Member 对话页面
import { useConversation } from "../hooks/useConversation";
import { MemberConversationContainer } from "../components/MemberConversationContainer";

export default function ConversationView() {
  const hook = useConversation();

  return <MemberConversationContainer {...hook} />;
}
