// Member 首页
import { useHome } from "../hooks/useHome";
import { MemberHomeContainer } from "../components/MemberHomeContainer";

export default function HomeView() {
  const hook = useHome();

  return <MemberHomeContainer {...hook} />;
}
